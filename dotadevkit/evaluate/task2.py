# --------------------------------------------------------
# dota_evaluation_task2
# Licensed under The MIT License [see LICENSE for details]
# Modified by Ashwin Nair
# Written by Jian Ding, based on code from Bharath Hariharan
# --------------------------------------------------------

import numpy as np
from dotadevkit.misc.dota_utils import dota_classes


def parse_gt(filename, version):
    objects = []
    with open(filename, "r") as f:
        lines = f.readlines()
        splitlines = [x.strip().split(" ") for x in lines]
        for splitline in splitlines:
            object_struct = {}
            if len(splitlines) < 9:
                continue
            object_struct["name"] = splitline[8]

            if version in ["1.5", "2.0"]:
                # DOTA 1.5 includes difficult annotations
                # by setting all annotations as easy
                object_struct["difficult"] = 0
            else:
                if len(splitlines) == 9:
                    object_struct["difficult"] = 0
                elif len(splitlines) == 10:
                    object_struct["difficult"] = int(splitlines[9])
            object_struct["difficult"] = 0
            object_struct["bbox"] = [
                int(float(splitline[0])),
                int(float(splitline[1])),
                int(float(splitline[4])),
                int(float(splitline[5])),
            ]
            w = int(float(splitline[4])) - int(float(splitline[0]))
            h = int(float(splitline[5])) - int(float(splitline[1]))
            object_struct["area"] = w * h
            objects.append(object_struct)
    return objects


def voc_ap(rec, prec, use_07_metric=False):
    """ap = voc_ap(rec, prec, [use_07_metric])
    Compute VOC AP given precision and recall.
    If use_07_metric is true, uses the
    VOC 07 11 point method (default:False).
    """
    if use_07_metric:
        # 11 point metric
        ap = 0.0
        for t in np.arange(0.0, 1.1, 0.1):
            if np.sum(rec >= t) == 0:
                p = 0
            else:
                p = np.max(prec[rec >= t])
            ap = ap + p / 11.0
    else:
        # correct AP calculation
        # first append sentinel values at the end
        mrec = np.concatenate(([0.0], rec, [1.0]))
        mpre = np.concatenate(([0.0], prec, [0.0]))

        # compute the precision envelope
        for i in range(mpre.size - 1, 0, -1):
            mpre[i - 1] = np.maximum(mpre[i - 1], mpre[i])

        # to calculate area under PR curve, look for points
        # where X axis (recall) changes value
        i = np.where(mrec[1:] != mrec[:-1])[0]

        # and sum (\Delta recall) * prec
        ap = np.sum((mrec[i + 1] - mrec[i]) * mpre[i + 1])
    return ap


def voc_eval(
    detpath, annopath, imagesetfile, classname, ovthresh=0.5, use_07_metric=False, version="1.0"
):
    """rec, prec, ap = voc_eval(detpath,
                                annopath,
                                imagesetfile,
                                classname,
                                [ovthresh],
                                [use_07_metric])
    Top level function that does the PASCAL VOC evaluation.
    detpath: Path to detections
        detpath.format(classname) should produce the detection results file.
    annopath: Path to annotations
        annopath.format(imagename) should be the xml annotations file.
    imagesetfile: Text file containing the list of images, one image per line.
    classname: Category name (duh)
    [ovthresh]: Overlap threshold (default = 0.5)
    [use_07_metric]: Whether to use VOC07's 11 point AP computation
        (default False)
    [version]: Version of DOTA (1.0 or 1.5)
    """
    # assumes detections are in detpath.format(classname)
    # assumes annotations are in annopath.format(imagename)
    # assumes imagesetfile is a text file with each line an image name

    # read list of images
    with open(imagesetfile, "r") as f:
        lines = f.readlines()
    imagenames = [x.strip() for x in lines]

    # load annots
    recs = {}
    for i, imagename in enumerate(imagenames):
        recs[imagename] = parse_gt(annopath.format(imagename), version)

    # extract gt objects for this class
    class_recs = {}
    npos = 0
    for imagename in imagenames:
        R = [obj for obj in recs[imagename] if obj["name"] == classname]
        bbox = np.array([x["bbox"] for x in R])
        difficult = np.array([x["difficult"] for x in R]).astype(np.bool)
        det = [False] * len(R)
        npos = npos + sum(~difficult)
        class_recs[imagename] = {"bbox": bbox, "difficult": difficult, "det": det}

    # read dets from Task2* files
    detfile = detpath.format(classname)
    with open(detfile, "r") as f:
        lines = f.readlines()

    splitlines = [x.strip().split(" ") for x in lines]
    image_ids = [x[0] for x in splitlines]
    confidence = np.array([float(x[1]) for x in splitlines])

    BB = np.array([[float(z) for z in x[2:]] for x in splitlines])

    # sort by confidence
    sorted_ind = np.argsort(-confidence)
    BB = BB[sorted_ind, :]
    image_ids = [image_ids[x] for x in sorted_ind]

    # go down dets and mark TPs and FPs
    nd = len(image_ids)
    tp = np.zeros(nd)
    fp = np.zeros(nd)
    for d in range(nd):
        R = class_recs[image_ids[d]]
        bb = BB[d, :].astype(float)
        ovmax = -np.inf
        BBGT = R["bbox"].astype(float)

        if BBGT.size > 0:
            # compute overlaps
            # intersection
            ixmin = np.maximum(BBGT[:, 0], bb[0])
            iymin = np.maximum(BBGT[:, 1], bb[1])
            ixmax = np.minimum(BBGT[:, 2], bb[2])
            iymax = np.minimum(BBGT[:, 3], bb[3])
            iw = np.maximum(ixmax - ixmin + 1.0, 0.0)
            ih = np.maximum(iymax - iymin + 1.0, 0.0)
            inters = iw * ih

            # union
            uni = (
                (bb[2] - bb[0] + 1.0) * (bb[3] - bb[1] + 1.0)
                + (BBGT[:, 2] - BBGT[:, 0] + 1.0) * (BBGT[:, 3] - BBGT[:, 1] + 1.0)
                - inters
            )

            overlaps = inters / uni
            ovmax = np.max(overlaps)
            # if there exist 2
            jmax = np.argmax(overlaps)

        if ovmax > ovthresh:
            if not R["difficult"][jmax]:
                if not R["det"][jmax]:
                    tp[d] = 1.0
                    R["det"][jmax] = 1
                else:
                    fp[d] = 1.0
        else:
            fp[d] = 1.0

    # compute precision recall

    print("check fp:", fp)
    print("check tp", tp)
    print("npos num:", npos)

    fp = np.cumsum(fp)
    tp = np.cumsum(tp)

    rec = tp / float(npos)
    # avoid divide by zero in case the first detection matches a difficult
    # ground truth
    prec = tp / np.maximum(tp + fp, np.finfo(np.float64).eps)
    ap = voc_ap(rec, prec, use_07_metric)

    return rec, prec, ap


def evaluate(detpath, annopath, imagesetfile, version="1.0"):
    assert version in ["1.0", "1.5", "2.0"]
    classnames = dota_classes
    if version == "1.5":
        classnames = classnames + ["container-crane"]
    if version == "2.0":
        classnames = classnames + ["container-crane", "airport", "helipad"]

    classaps = []
    map = 0
    for classname in classnames:
        print("classname:", classname)
        rec, prec, ap = voc_eval(
            detpath,
            annopath,
            imagesetfile,
            classname,
            ovthresh=0.5,
            use_07_metric=True,
            version=version,
        )
        map = map + ap
        # print('rec: ', rec, 'prec: ', prec, 'ap: ', ap)
        print("ap: ", ap)
        classaps.append(ap)

        # umcomment to show p-r curve of each category
        # plt.figure(figsize=(8,4))
        # plt.xlabel('recall')
        # plt.ylabel('precision')
        # plt.plot(rec, prec)
    # plt.show()
    map = map / len(classnames)
    print("map:", map)
    classaps = 100 * np.array(classaps)
    print("classaps: ", classaps)


if __name__ == "__main__":
    detections = (
        r"/home/ashwin/Desktop/Projects/DOTA_devkit/examplesplit/labelTxt_remerged/Task2_{:s}.txt"
    )
    annotations = r"/home/ashwin/Desktop/Projects/rasterdet/data/dota/val/labelTxt/{:s}.txt"
    images = r"/home/ashwin/Desktop/Projects/rasterdet/data/dota/val/val.txt"
    evaluate(detections, annotations, images, "1.0")
