from PIL import Image, ImageDraw, ImageColor, ImageFont
from data_provider import get_data_base_object
import datetime
import os

con = get_data_base_object()


def get_dates():
    today = datetime.datetime.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    dates_this_week = [start_of_week + datetime.timedelta(days=i) for i in range(7)]
    formatted_dates = [date.strftime('%d.%m') for date in dates_this_week]
    return formatted_dates


def create_empty(user_id, width, height, message, name):
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    list_cor_x = [width * cor // 10 for cor in range(2, 9)]
    list_cor_y = [height * cor // 10 for cor in range(3, 8)]
    days = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
    dates = get_dates()

    for i in range(len(list_cor_y)):
        draw.line((list_cor_x[0], list_cor_y[i], list_cor_x[-1], list_cor_y[i]), fill=ImageColor.getrgb("#F0F0F0"),
                  width=2)
    for j in range(len(list_cor_x)):
        draw.line((list_cor_x[j], list_cor_y[0], list_cor_x[j], list_cor_y[-1]), fill=ImageColor.getrgb("#F0F0F0"),
                  width=2)

    font1 = ImageFont.truetype("resources/fonts//Montserrat_r.ttf", 30)
    font2 = ImageFont.truetype("resources/fonts//Montserrat.ttf", 15)
    draw.text((width * 2 // 10 - 50, height * 2 // 10 - 40), message, (50, 50, 50), font=font1)

    text_w = font2.getlength(days[0])

    for i in range(len(list_cor_x)):
        draw.text((list_cor_x[i] - text_w // 2 + 2, list_cor_y[-1] + height // 20), days[i], (100, 100, 100),
                  font=font2)
        draw.text((list_cor_x[i] - text_w // 2 + 2 - 7, list_cor_y[-1] + height // 20 + 20), dates[i], (100, 100, 100),
                  font=font2)

    im1, im2, im3, im4, im5 = Image.open("resources/pictures/1.png"), Image.open(
        "resources/pictures/2.png"), Image.open(
        "resources/pictures/3.png"), \
        Image.open("resources/pictures/4.png"), Image.open("resources/pictures/5.png")
    im1.thumbnail(size=(30, 30))
    im2.thumbnail(size=(30, 30))
    im3.thumbnail(size=(30, 30))
    im4.thumbnail(size=(30, 30))
    im5.thumbnail(size=(30, 30))
    list_im = [im5, im4, im3, im2, im1]

    for i in range(5):
        image.paste(list_im[i], (list_cor_x[0] - 50, list_cor_y[i] - 15), mask=list_im[i])

    image.save('resources/files//' + str(user_id) + "_" + name + ".png", "PNG")
    image.close()

    return 'resources/files//' + str(user_id) + "_" + name + ".png"


def draw_point(path, width, height, day, mark):
    image = Image.open(path)
    draw = ImageDraw.Draw(image)

    list_cor_x = [width * cor // 10 for cor in range(2, 9)]
    list_cor_y = [height * cor // 10 for cor in range(3, 8)]

    draw.ellipse((list_cor_x[day] - 8, list_cor_y[4 - mark] - 8, list_cor_x[day] + 8, list_cor_y[4 - mark] + 8),
                 fill=ImageColor.getcolor("#FF8C00", "RGB"), width=5)

    image.save(path, "PNG")


def draw_graph(path, width, height, list_points):
    image = Image.open(path)
    draw = ImageDraw.Draw(image)

    list_cor_x = [width * cor // 10 for cor in range(2, 9)]
    list_cor_y = [height * cor // 10 for cor in range(3, 8)]

    list_del = []
    for i in range(len(list_points)):
        if list_points[i][1] != -1:
            draw_point(path, width, height, list_points[i][0], list_points[i][1])
        else:
            list_del.append(i)
    for i in list_del[::-1]:
        del list_points[i]

    for i in range(len(list_points) - 1):
        draw.line((list_cor_x[list_points[i][0]], list_cor_y[4 - list_points[i][1]], list_cor_x[list_points[i + 1][0]],
                   list_cor_y[4 - list_points[i + 1][1]]), fill=ImageColor.getrgb("#FF8C00"), width=3)

    image.save(path, "PNG")
    image.close()


def create_graphs(user_id):
    global con
    size_x, size_y = 1000, 600
    graph_name = ['mood', 'calmness', 'productivity', 'environment', 'self_confidence', 'pacification',
                  'self_satisfaction']
    table_name = ['MOOD', 'CALMNESS', 'PRODUCTIVITY', 'ENVIRONMENT', 'SELF_CONFIDENCE', 'PACIFICATION',
                  'SELF_SATISFACTION']
    title_name = ['Настроение (Как прошел день?)', 'Спокойствие', 'Продуктивность',
                  'Окружение (Преследовало ли одиночество?)', 'Уверенность в себе',
                  'Умиротворение (Раздражало ли что-то?)', 'Удовлетворенность собой']
    for i in range(7):
        path = create_empty(user_id, size_x, size_y, title_name[i], graph_name[i])
        with con:
            all_data = list(con.execute(f"SELECT score, date FROM CheckUp WHERE user_id='{user_id}' and "
                                        f"type_of_graph='{table_name[i]}'"))
            lst = [-1, -1, -1, -1, -1, -1, -1]
            for x in range(7):
                if len(all_data) > x:
                    if datetime.date(int(all_data[x][1][:4]), int(all_data[x][1][5:7]),
                                     int(all_data[x][1][8:])).isocalendar()[1] == \
                            datetime.datetime.today().isocalendar()[1]:
                        lst[datetime.date(int(all_data[x][1][:4]), int(all_data[x][1][5:7]),
                                          int(all_data[x][1][8:])).weekday()] = \
                            all_data[x][0]
            lt = [(i, lst[i]) for i in range(7)]
        draw_graph(path, size_x, size_y, lt)


def photo_del(user_id):
    os.remove("resources//files//" + str(user_id) + "_mood.png")
    os.remove("resources//files//" + str(user_id) + "_calmness.png")
    os.remove("resources//files//" + str(user_id) + "_productivity.png")
    os.remove("resources//files//" + str(user_id) + "_environment.png")
    os.remove("resources//files//" + str(user_id) + "_self_confidence.png")
    os.remove("resources//files//" + str(user_id) + "_pacification.png")
    os.remove("resources//files//" + str(user_id) + "_self_satisfaction.png")


# create_empty(1, 1000, 600, 'График настроения', '')
# draw_graph('example.png', 1000, 600, [[0, 4], [1, 4], [2, 3], [3, 2], [4, 4], [5, 0], [6, 4]])
# photo_del(596752948)
