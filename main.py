import cv2
import copy


def count_object(
    img: cv2.UMat, min_area: float, t1: float, t2: float
) -> (int, cv2.UMat):
    img_cpy = copy.deepcopy(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, t1, t2)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    count = 0
    min_area = min_area
    for contour in contours:
        if cv2.contourArea(contour) >= min_area:
            count += 1
            cv2.drawContours(img_cpy, [contour], -1, (0, 255, 0), 2)
    return count, img_cpy


original = None
contour = None
count = 0
semut = None
bakteri = None


def on_change(val):
    global contour, count

    lower = cv2.getTrackbarPos("Lower", "Edges")
    upper = cv2.getTrackbarPos("Upper", "Edges")
    area = cv2.getTrackbarPos("Area", "Edges")
    switch = cv2.getTrackbarPos("Switch", "Edges")

    if switch == 0:
        original = semut
    else:
        original = bakteri

    count, contour = count_object(original, area, lower, upper)

    cv2.putText(
        contour,
        f"count = {count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )

    cv2.imshow("Edges", contour)
    cv2.imshow("Original", original)

    print(count)


def main():
    global original, contour, count, semut, bakteri

    semut = cv2.imread("./image/edge_detection_1.jpg")
    bakteri = cv2.imread("./image/edge_detection_2.jpg")

    original = semut

    count, contour = count_object(original, 10, 0, 100)
    print(count)

    cv2.imshow("Edges", contour)
    cv2.imshow("Original", original)

    cv2.createTrackbar("Switch", "Edges", 0, 1, on_change)
    cv2.createTrackbar("Lower", "Edges", 50, 255, on_change)
    cv2.createTrackbar("Upper", "Edges", 150, 255, on_change)
    cv2.createTrackbar("Area", "Edges", 10, 255, on_change)

    cv2.waitKey(0)
    cv2.destroyAllWindows


if __name__ == "__main__":
    main()
