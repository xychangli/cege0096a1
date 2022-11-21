from plotter import Plotter

def get_mbr(polygon): # Input polygon: [[xa, ya], [xb, yb]]. Returns the MBR

    polygon_x = [] # Empty list for all x and y coordinates
    polygon_y = []

    for i in range(len(polygon)): # For loop to iterate through all polygon points, add x and y to lists
        polygon_x.append(polygon[i][0])
        polygon_y.append(polygon[i][1])

    point_0 = [max(polygon_x), max(polygon_y)] # Find the max and min of x and y, make them into MBR polygon with same format
    point_1 = [max(polygon_x), min(polygon_y)]
    point_2 = [min(polygon_x), min(polygon_y)]
    point_3 = [min(polygon_x), max(polygon_y)]
    mbr = [point_0, point_1, point_2, point_3, point_0]

    return mbr # Return the MBR [x, y] list

def is_point_in_polygon(point, polygon): # Point: [[xp, yp]], Polygon: [[xa, ya], [xb, yb]]

    mbr = get_mbr(polygon)
    outside = []
    inside = []
    boundary = []

    for i in range(len(point)): # For all points

        # mbr[0][0] = Max X, mbr[2][0] = Min X, mbr[0][1] = Max Y, mbr[2][1] = Min Y
        # If point is outside the MBR, it could be classified as outside
        if point[i][0] > mbr[0][0] or point[i][0] < mbr[2][0] or point[i][1] > mbr[0][1] or point[i][1] < mbr[2][1]:
            outside.append(point[i])

        # If point is inside (including boundaries) of the MBR
        else:
            count = 0 # Set intersection count to Zero
            start = polygon[0] # Set start point

            for j in range(1, len(polygon)): # For all polygon points, -1 to not exceed maximum length
                end = polygon[j]
                # Imagine Ray going directly up, line X = point_x,
                # If the intersection of X = point_x and line of polygon is above the actual point, ray does intersect with line
                # If the intersection's Y value is lower than point_y, ray does not intersect, Y of actual point = point[i][1]
                # Do special cases

                if point[i][0] == start[0] and point[i][1] == start[1]: # If point is on end points
                    boundary.append(point[i])

                elif start[0] == end[0]: # If Vertical line
                    line_mbr = get_mbr([start, end]) # Get two point MBR

                    if point[i][0] == start[0]:
                        if point[i][1] < line_mbr[0][1] and point[i][1] > line_mbr[2][1]: # If it is within the MBR, no end points, Y is between max and min
                            boundary.append(point[i])
                    elif point[i][0] < start[0]:
                        if point[i][1] < line_mbr[0][1] and point[i][1] > line_mbr[2][1]:
                            count += 1

                elif start[1] == end[1]: # If Horizontal line
                    line_mbr = get_mbr([start, end]) # Get two point MBR

                    if point[i][1] == start[1]:
                        if point[i][0] < line_mbr[0][0] and point[i][0] > line_mbr[2][0]: # If it is within the MBR, no end points, X is between max and min
                            boundary.append(point[i])
                        elif point[i][0] < line_mbr[2][0]:
                            count += 1

                elif start[0] != end[0] and start[1] != end[1]: # If on all other lines
                    line_mbr = get_mbr([start, end]) # Get two point MBR

                    if point[i][1] == (point[i][0] - start[0]) / (end[0] - start[0]) * (end[1] - start[1]) + start[1]: # Check if it satisfies the formula of two points
                        if point[i][0] < line_mbr[0][0] and point[i][0] > line_mbr[2][0]: # If it is within the MBR, no end points
                            boundary.append(point[i])
                    elif (end[1] > start[1] and end[0] > start[0]) or (end[1] < start[1] and end[0] < start[0]): # If it is an upward line
                        if point[i][1] > (point[i][0] - start[0]) / (end[0] - start[0]) * (end[1] - start[1]) + start[1]:
                            if point[i][0] < line_mbr[0][0] and point[i][0] > line_mbr[2][0]: # If it is within the MBR, no end points
                                count += 1
                    elif (end[1] < start[1] and end[0] > start[0]) or (end[1] > start[1] and end[0] < start[0]): # If it is an downward line
                        if point[i][1] < (point[i][0] - start[0]) / (end[0] - start[0]) * (end[1] - start[1]) + start[1]:
                            if point[i][0] < line_mbr[0][0] and point[i][0] > line_mbr[2][0]: # If it is within the MBR, no end points
                                count += 1
                start = end # Let new start point be the previous end point

            if count % 2 == 0:
                outside.append(point[i])
            elif count % 2 != 0:
                inside.append(point[i])



    status = [outside, inside, boundary]

    return status # Return the status of points


def main():
    plotter = Plotter()
    print('read polygon.csv')
    polygon = []
    with open('polygon.csv', 'r') as polygon_file:
        polygon_file.readline()
        for line in polygon_file:
            polygon_line = line.rstrip('\n').split(',')
            polygon_line.pop(0)
            polygon_line = list(map(float, polygon_line))
            polygon.append(polygon_line)

    print('Insert point information')
    x = float(input('x coordinate: '))
    y = float(input('y coordinate: '))
    point = []
    point.append([x, y])


    print('categorize point')
    result = is_point_in_polygon(point, polygon)
    if point in result[0]:
        print('outside')
    elif point in result[1]:
        print('inside')
    else:
        print('boundary')

    print('plot polygon and point')
    polygon_x = []
    polygon_y = []
    point_x = []
    point_y = []
    for i in range(len(polygon)):
        polygon_x.append(polygon[i][0])
        polygon_y.append(polygon[i][1])
    for i in range(len(point)):
        point_x.append(point[i][0])
        point_y.append(point[i][1])


    plotter.add_polygon(polygon_x, polygon_y)
    plotter.add_point(point_x, point_y)
    plotter.show()


if __name__ == '__main__':
    main()
