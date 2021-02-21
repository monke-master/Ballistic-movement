from tkinter import *
from kinematics import *
from tkinter.messagebox import *


class Window:
    __window = None
    __currWindow = 1
    __type = None
    __currComponents = list()
    __data = dict()
    __known = dict()
    __unknown = dict()
    __accuracy = None

    def __init__(self):
        self.__window = Tk()
        self.__window.title("Моделирование траектории броска")
        self.__window.resizable(0, 0)
        self.__window.geometry('600x300')
        self.__setWindow()

    def __setWindow1(self):  # сделать красивее!!!
        self.__window.geometry('600x300')
        self.__type = IntVar()
        self.__type.set(1)

        greet_lbl = Label(text="Вас приветствует программа по моделированию траектории брошенного тела\n"
                               "Выберите тип броска:", font='arial 12')
        greet_lbl.place(relx=0.0215, rely=0.1)

        ct1 = Radiobutton(text='1.Под углом к горизонту', font='arial 12', variable=self.__type, value=1)
        ct1.place(relx=0.34, rely=0.25)

        ct2 = Radiobutton(text='2.Вертикально вверх', font='arial 12', variable=self.__type, value=2)
        ct2.place(relx=0.34, rely=0.35)

        ct3 = Radiobutton(text='3.Горизонтально', font='arial 12', variable=self.__type, value=3)
        ct3.place(relx=0.34, rely=0.45)

        btn_next = Button(text='Далее', font='arial 12', command=self.__nextWindow)
        btn_next.place(relx=0.85, rely=0.85)

        self.__currComponents.append(greet_lbl)
        self.__currComponents.append(ct1)
        self.__currComponents.append(ct2)
        self.__currComponents.append(ct3)
        self.__currComponents.append(btn_next)

    def __setWindow2(self):  # сделать красивее!!!
        self.__window.geometry('600x300')
        btn_prev = Button(text='Назад', font='arial 12', command=self.__prevWindow)
        btn_prev.place(relx=0.05, rely=0.85)

        btn_next = Button(text='Далее', font='arial 12', command=self.__nextWindow)
        btn_next.place(relx=0.85, rely=0.85)

        lbl_inst = Label(text='Введите известные данные. Если данных нет, оставьте поле пустым', font='arial 12')
        lbl_inst.place(relx=0.01, rely=0.01)

        lbl_speed = Label(text='Начальная скорость(м/с)', font='arial 12')
        lbl_speed.place(relx=0.01, rely=0.1)

        speed = StringVar()
        entry_speed = Entry(textvariable=speed)
        entry_speed.place(relx=0.4, rely=0.1)
        self.__data['speed'] = speed

        lbl_height = Label(text='Высота броска(м)', font='arial 12')
        lbl_height.place(relx=0.01, rely=0.2)

        height = StringVar()
        entry_height = Entry(textvariable=height)
        entry_height.place(relx=0.4, rely=0.2)
        self.__data['height'] = height

        lbl_time = Label(text='Время полёта(с)', font='arial 12')
        lbl_time.place(relx=0.01, rely=0.3)

        time = StringVar()
        entry_time = Entry(textvariable=time)
        entry_time.place(relx=0.4, rely=0.3)
        self.__data['time'] = time

        lbl_max_height = Label(text='Максимальная высота(м)', font='arial 12')
        lbl_max_height.place(relx=0.01, rely=0.4)

        max_height = StringVar()
        entry_max_height = Entry(textvariable=max_height)
        entry_max_height.place(relx=0.4, rely=0.4)
        self.__data['max_height'] = max_height

        if self.__type.get() != 2:
            lbl_distance = Label(text='Дальность полета(м)', font='arial 12')
            lbl_distance.place(relx=0.01, rely=0.5)
            distance = StringVar()
            entry_distance = Entry(textvariable=distance)
            entry_distance.place(relx=0.4, rely=0.5)
            self.__data['distance'] = distance
            self.__currComponents.append(lbl_distance)
            self.__currComponents.append(entry_distance)

        if self.__type.get() == 1:
            lbl_angle = Label(text='Угол(в градусах)', font='arial 12')
            lbl_angle.place(relx=0.01, rely=0.6)
            angle = StringVar()
            entry_angle = Entry(textvariable=angle)
            entry_angle.place(relx=0.4, rely=0.6)
            self.__data['angle'] = angle
            self.__currComponents.append(entry_angle)
            self.__currComponents.append(lbl_angle)

        lbl_accur = Label(text='Точность вычислений\n'
                               '(знаков после запятой)', font='arial 12')
        lbl_accur.place(relx=0.6, rely=0.1)
        self.__accuracy = StringVar()
        self.__accuracy.set('2')
        entry_accur = Entry(textvariable=self.__accuracy)
        entry_accur.place(relx=0.9, rely=0.1)
        self.__currComponents.append(entry_accur)
        self.__currComponents.append(lbl_accur)
        self.__currComponents.append(lbl_inst)
        self.__currComponents.append(lbl_height)
        self.__currComponents.append(entry_height)
        self.__currComponents.append(lbl_speed)
        self.__currComponents.append(entry_speed)
        self.__currComponents.append(lbl_time)
        self.__currComponents.append(entry_time)
        self.__currComponents.append(lbl_max_height)
        self.__currComponents.append(entry_max_height)
        self.__currComponents.append(btn_prev)
        self.__currComponents.append(btn_next)

    def __setWindow3(self):  # сделать красивее!!!
        self.__window.geometry('800x800')
        btn_prev = Button(text='Назад', font='arial 12', command=self.__prevWindow)
        btn_prev.place(relx=0.05, rely=0.95)
        if self.__type.get() == 1:
            self.__atAngle()
        if self.__type.get() == 2:
            self.__verticalUp()

        self.__currComponents.append(btn_prev)

    def __atAngle(self):
        acc = '.' + str(self.__accuracy.get()) + 'f'
        answer = ''
        v0 = h = S = H = alpha = tf = None
        for key in self.__unknown:
            if key == 'speed':
                if 'angle' in self.__known and 'height' in self.__known and 'max_height' in self.__known:
                    H = float(self.__known['max_height'])
                    alpha = float(self.__known['angle'])
                    h = float(self.__known['height'])
                    v0 = float(format(v0_from_H_a_h(H, alpha, h), acc))
                    self.__known['speed'] = v0
                    s = 'Найдем время подъема на максимальную высоту: Vy(tпод) = v0*sin(a) - gt = 0 => tпол=\n' \
                        'v0*sin(a)/g. H = y(tпод) = h + v0*sin(a)*tпод - g*tпод^2/2. Подставляем tпод и выражаем v0:\n' \
                        'v0=sqrt(2*g*(H-h)/sin(a))= ' + format(v0, acc) + '\n'
                    answer += s
                elif 'time' in self.__known and 'height' in self.__known and 'angle' in self.__known:
                    h = float(self.__known['height'])
                    alpha = float(self.__known['angle'])
                    tf = float(self.__known['time'])
                    v0 = float(format(v0_from_h_a_tf(h, alpha, tf), acc))
                    self.__known['speed'] = v0
                    s = 'Координата по y в момент времени tпол равна нулю: y(tпол) = h + vo*sin(a)*tпол - g*tпол^2/2 = 0\n' \
                        'Найдем отсюда v0:0=g*tпол/2sin(a) - h/sin(a)пол*t = ' + format(v0, acc) + '\n'
                    answer += s
                elif 'time' in self.__known and 'distance' in self.__known and 'angle' in self.__known:
                    S = float(self.__known['distance'])
                    alpha = float(self.__known['angle'])
                    tf = float(self.__known['time'])
                    v0 = float(format(vo_from_S_a_tf(S, alpha, tf), acc))
                    self.__known['speed'] = v0
                    s = 'Дальность полета S равна координате по Х в помент времени tпол: S = x(tпол) = v0*cos(a)*tпол => \n' \
                        'v0 = s/cos(a)*tпол = ' + format(v0, acc) + '\n'
                    answer += s
                elif 'time' in self.__known and 'max_height' in self.__known and 'angle' in self.__known:
                    H = float(self.__known['max_height'])
                    alpha = float(self.__known['angle'])
                    tf = float(self.__known['time'])
                    v0 = float(format(v0_from_H_a_tf(H, alpha, tf), acc))
                    self.__known['speed'] = v0
                    s = 'Максимальная высота находится по формуле H = h + v0^2*sin(a)^2/2g (1). y(tпол) = h + v0*sin(a)*tпол- \n' \
                        '- g*tпол^2/2 (2). Выразим из (1) h и подставим во (2), приведя к квадратному уравнению относительно v0.\n' \
                        'Решим его, получаем v0 = (g*tпол + sqrt(2gH))/sin(a) = ' + format(v0, acc) + '\n'
                    answer += s
                elif 'max_height' in self.__known and 'angle' in self.__known and 'distance' in self.__known:
                    H = float(self.__known['max_height'])
                    S = float(self.__known['distance'])
                    alpha = float(self.__known['angle'])
                    v0 = float(format(v0_from_H_a_S(H, alpha, S), acc))
                    self.__known['speed'] = v0
                    s = 'Максимальная высота находится по формуле H = h + v0^2*sin(a)^2/2g (1). Время полета находится\n' \
                        'по формуле: tпол = (v0*sin(a) + sqrt(2*g*h + v0*v0*sin(a)*sin(a)))/g (2). Подставим (1) во (2) и найдем v0:\n' \
                        'v0 = (sqrt(2*cos(a)**2*g*H + 2*g*S*sin(2*a)) - cos(a)*sqrt(2*g*H)) / sin(2*a) = ' + format(v0, acc) + '\n'
                    answer += s
                elif 'height' in self.__known and 'time' in self.__known and 'distance' in self.__known:
                    h = float(self.__known['height'])
                    S = float(self.__known['distance'])
                    tf = float(self.__known['time'])
                    v0 = float(format(v0_from_h_tf_S(h, tf, S), acc))
                    self.__known['speed'] = v0
                    s = 'Дальность полета S равна координате по Х в помент времени tпол: S = x(tпол) = v0*cos(a)*tпол.\n' \
                        'Выразим косинус через синус и найдем его квадрат: sin(a)^2 = 1 - (t/sv0)^2 (1). Время полета\n' \
                        'находится по формуле tпол = (v0*sin(a) + sqrt(v0^2*sin(a)^2 + 2gh)) /g (2). Выразим из этой\n' \
                        'Формулы синус и подставим в (1). Из полученного уравнения находим: \n' \
                        '            v0 = sqrt(s^2(g*t^2-2h)^2 + 4t^4)/ts =  ' + format(v0, acc) + '\n'
                    answer += s
                elif 'height' in self.__known and 'distance' in self.__known and 'angle' in self.__known:
                    h = float(self.__known['height'])
                    S = float(self.__known['distance'])
                    alpha = float(self.__known['angle'])
                    v0 = float(format(v0_from_S_a_h(S, alpha, h), acc))
                    self.__known['speed'] = v0
                    s = 'Дальность полета S равна координате по Х в помент времени tпол: S=x(tпол)=v0*cos(a)*tпол(1)\n'\
                        'Время полета находится по формуле tпол = (v0*sin(a) + sqrt(v0^2*sin(a)^2 + 2gh)) /g (2) \n' \
                        'Подставим (2) в (1) и выразим v0: v0=(sqrt(cos(a)^2*h^2+10*S^3*sin(2*a))-cos(a)*h)/Ssin(2*a)=' \
                        + format(v0, acc) + '\n'
                    answer += s
                elif 'max_height' in self.__known and 'time' in self.__known:
                    s = 'В данном случае скорость найти нельзя'
                    answer += s
                else:
                    self.__setWindow2()
                    self.__throw_error('В данном случае невозможно решить задачу')
            if key == 'height':
                if 'speed' in self.__known:
                    v0 = float(self.__known['speed'])
                if 'max_height' in self.__known and 'angle' in self.__known:
                    alpha = float(self.__known['angle'])
                    H = float(self.__known['max_height'])
                    h = float(format(h_from_v0_H_a(v0, H, alpha), acc))
                    self.__known['height'] = h
                    s = 'Высоту броска h найдем из формулы максимальной высоты:  H = h + V0^2*sin(a)^2/2g => \n' \
                        'h = H - V0^2*sin(a)^2/2g = ' + format(h, acc) + '\n'
                    answer += s
                elif 'distance' in self.__known and 'angle' in self.__known:
                    alpha = float(self.__known['angle'])
                    S = float(self.__known['distance'])
                    h = float(format(h_from_v0_S_a(v0, S, alpha), acc))
                    self.__known['height'] = h
                    s = 'Дальность полета S равна координате по Х в помент времени tпол: S=x(tпол)=v0*cos(a)*tпол(1)\n'\
                        'Время полета находится по формуле tпол = (v0*sin(a) + sqrt(v0^2*sin(a)^2 + 2gh)) /g (2) \n' \
                        'Подставим (2) в (1) и выразим h: h = g*S^2/(2*v0^2*cos(a)^2) - tan(a)*S = ' + format(h, acc) \
                        + '\n'
                    answer += s
                elif 'distance' in self.__known and 'time' in self.__known:
                    S = float(self.__known['distance'])
                    tf = float(self.__known['time'])
                    alpha = alpha_from_S_tf_v0(S, tf, v0)
                    self.__known['angle'] = alpha
                    h = float(format(h_from_v0_S_a(v0, S, alpha), acc))
                    self.__known['height'] = h
                    s = 'Найдем угол броска из формулы дальности полета: S = V0*cos(a)*tпол => \n' \
                        'a = arccos(S/v0*tпол) = ' + format(alpha, acc) + '. Теперь найдем h.\n' \
                        'Дальность полета S равна координате по Х в помент времени tпол: S=x(tпол)=v0*cos(a)*tпол(1)\n'\
                        'Время полета находится по формуле tпол = (v0*sin(a) + sqrt(v0^2*sin(a)^2 + 2gh)) /g (2) \n' \
                        'Подставим (2) в (1) и выразим h: h = g*S^2/(2*v0^2*cos(a)^2) - tan(a)*S = ' + format(h, acc) \
                        + '\n'
                    answer += s
                elif 'max_height' in self.__known and 'time' in self.__known:
                    H = float(self.__known['max_height'])
                    tf = float(self.__known['time'])
                    h = float(format(h_from_H_tf(H, tf), acc))
                    self.__known['height'] = h
                    s = 'Запишем формулы максимальной высоты H = h + V0^2*sin(a)^2/2g и времени полета tпол = \n' \
                        '(v0*sin(a)+(v0^2*sin(a)^2 + 2gh))/g.В ыразим из второй формулы sin(a) и подставим в первую.\n'\
                        'Решаем квадратное уравнение относительно h: = ((32*g*t*t*H)^0.5-2*g*t*t)/4 = ' + str(h) + '\n'
                    answer += s
                elif 'time' in self.__known and 'angle' in self.__known:
                    tf = float(self.__known['time'])
                    alpha = float(self.__known['angle'])
                    h = float(format(h_from_v0_tf_a(v0, tf, alpha), acc))
                    self.__known['height'] = h
                    s = 'Запишем формулу времени полета tпол=(v0*sin(a)+(v0^2*sin(a)^2 + 2gh))/g. Выразим отсюда h: \n'\
                        'h = (g*t^2 - 2*v0*sin(a)*t)/2 = ' + format(h, acc) + '\n'
                    answer += s
                else:
                    self.__setWindow2()
                    self.__throw_error('В данном случае невозможно решить задачу')
            if key == 'angle':
                if 'speed' in self.__known:
                    v0 = float(self.__known['speed'])
                if 'height' in self.__known:
                    h = float(self.__known['height'])
                if 'max_height' in self.__known:
                    H = float(self.__known['max_height'])
                    alpha = float(format(alpha_from_H_h_v0(H, h, v0), acc))
                    self.__known['angle'] = alpha
                    s = 'Найдем угол a из формулы максимальной высоты: H = h + V0^2*sin(a)^2/2g => \n' \
                        'a = arcsin((2*g*(H-h))^0.5 / v0) = ' + str(alpha) + '\n'
                    answer += s
            if key == 'max_height':
                pass
            if key == 'time':
                pass
            if key == 'distance':
                pass
        decision = Label(text=answer, font='arial 12', anchor='e')
        decision.place(relx=0.01, rely=0.1)
        self.__currComponents.append(decision)

    def __verticalUp(self):
        acc = '.' + str(self.__accuracy.get()) + 'f'
        if 'height' in self.__known and 'speed' in self.__known:  # ИСПРАВИТЬ!!!!!!!Й!!!
            h = float(self.__known['height'])
            v0 = float(self.__known['speed'])
            tf = find_tf(h, v0, 90)
            H = find_Hmax(h, v0, 90)
            given = Label(text='Дано:\n'
                                'v0=' + str(v0) + '\n'
                                'h=' + str(h) + '\n'
                                'Решение:', font='arial 12', anchor='e')
            given.place(relx=0.01, rely=0.01)
            s = "Время полета тела найдем из уравнения y(tпол) = h + v0*tпол - g*tпол^2/2 = 0. " \
                "Решая квадратное уравнение\n относительно tпол находим " \
                "tпол = (V0 + (g*h + V0^2)^0.5)/g =" + format(tf, acc) + "\n" \
                "Максимальная высота подъема H находится из кинематического уравнения \n" \
                "H = y(tпод) = h + V0*tпод - g*t^2/2, где tпод - время подъема на высоту H\n" \
                "Vy(tпод) = V0 - g*tпод => tпод = v0/g. Подставим в предыдущее уравнение: \n" \
                "H = h + V0^2/2g = " + format(H, acc)
            decision = Label(text=s, font='arial 12', anchor='e')
            decision.place(relx=0.01, rely=0.1)
            self.__currComponents.append(given)
            self.__currComponents.append(decision)
        if 'height' in self.__known and 'time' in self.__known:
            tf = float(self.__data['time'])
            h = float(self.__known['height'])
            v0 = find_v0y(h, tf)
            H = find_Hmax(h, v0, 90)
            given = Label(text='Дано:\n'
                               'tпол=' + str(tf) + '\n'
                               'h=' + str(h) + '\n'
                               'Решение:', font='arial 12', anchor='e')
            given.place(relx=0.01, rely=0.01)
            s = "Начальную скорость найдем из уравнения y(tпол) = h + v0*tпол - g*tпол^2/2 = 0\n" \
                "Выражаем отсюда скорость: v0 = g*t/2 - h/2 = " + format(v0, acc) + "\n" \
                "Максимальная высота подъема H находится из кинематического уравнения \n" \
                "H = y(tпод) = h + V0*tпод - g*t^2/2, где tпод - время подъема на высоту H\n" \
                "Vy(tпод) = V0 - g*tпод => tпод = v0/g. Подставим в предыдущее уравнение: \n" \
                "H = h + V0^2/2g = " + format(H,acc)
            decision = Label(text=s, font='arial 12', anchor='e')
            decision.place(relx=0.01, rely=0.1)
            self.__currComponents.append(given)
            self.__currComponents.append(decision)
        if 'height' in self.__known and 'max_height' in self.__known:
            H = float(self.__data['max_height'])
            h = float(self.__known['height'])
            v0 = find_v0y_from_H(h, H, 90)
            tf = find_tf(h, v0, 90)
            given = Label(text='Дано:\n'
                               'H=' + str(H) + '\n'
                               'h=' + str(h) + '\n'
                               'Решение:', font='arial 12', anchor='e')
            given.place(relx=0.01, rely=0.01)
            s = "Максимальная высота подъема H находится из кинематического уравнения \n" \
                "H = y(tпод) = h + V0*tпод - g*t^2/2, где tпод - время подъема на высоту H\n" \
                "Vy(tпод) = V0 - g*tпод => tпод = v0/g. Подставим в предыдущее уравнение: \n" \
                "H = h + V0^2/2g. Выразим отсюда скорость: v0 = (2*g(H-h))^0.5 = " + format(v0, acc) + "\n" \
                "Время полета тела найдем из уравнения y(tпол) = h + v0*tпол - g*tпол^2/2 = 0. " \
                "Решая квадратное уравнение\n относительно tпол находим " \
                "tпол = (V0 + (g*h + V0^2)^0.5)/g =" + format(tf, acc)
            decision = Label(text=s, font='arial 12', anchor='e')
            decision.place(relx=0.01, rely=0.1)
            self.__currComponents.append(given)
            self.__currComponents.append(decision)
        if 'speed' in self.__known and 'time' in self.__known:
            v0 = float(self.__known['speed'])
            tf = float(self.__data['time'])
            h = find_h(v0, tf)
            H = find_Hmax(h, v0, 90)
            given = Label(text='Дано:\n'
                               'v0=' + str(v0) + '\n'
                               'tпол=' + str(tf) + '\n'
                               'Решение:', font='arial 12', anchor='e')
            given.place(relx=0.01, rely=0.01)
            s = "Высота броска h находится из кинематического уравнения по оси Y в момент времени tпол:\n" \
                "y(tпол) = h + v0*t - g*t*t/2 = 0 => h = g*t*t/2 - v0*t = " + format(h, acc) + "\n" \
                "Максимальная высота подъема H находится из кинематического уравнения \n" \
                "H = y(tпод) = h + V0*tпод - g*t^2/2, где tпод - время подъема на высоту H\n" \
                "Vy(tпод) = V0 - g*tпод => tпод = v0/g. Подставим в предыдущее уравнение: \n" \
                "H = h + V0^2/2g = " + format(H, acc)
            decision = Label(text=s, font='arial 12', anchor='e')
            decision.place(relx=0.01, rely=0.1)
            self.__currComponents.append(given)
            self.__currComponents.append(decision)
        if 'speed' in self.__known and 'max_height' in self.__known:
            v0 = float(self.__known['speed'])
            H = float(self.__data['max_height'])
            h = find_h_from_H(v0, H)
            tf = find_tf(h, v0, 90)
            given = Label(text='Дано:\n'
                               'v0=' + str(v0) + '\n'
                               'H=' + str(H) + '\n'
                               'Решение:', font='arial 12', anchor='e')
            given.place(relx=0.01, rely=0.01)
            s = "Максимальная высота подъема H находится из кинематического уравнения \n" \
                "H = y(tпод) = h + V0*tпод - g*t^2/2, где tпод - время подъема на высоту H\n" \
                "Vy(tпод) = V0 - g*tпод => tпод = v0/g. Подставим в предыдущее уравнение: \n" \
                "H = h + V0^2/2g => h = H - v0^2/2g = " + format(h, acc) + '\n' \
                "Время полета тела найдем из уравнения y(tпол) = h + v0*tпол - g*tпол^2/2 = 0. " \
                "Решая квадратное уравнение\n относительно tпол находим " \
                "tпол = (V0 + (g*h + V0^2)^0.5)/g =" + format(tf, acc)
            decision = Label(text=s, font='arial 12', anchor='e')
            decision.place(relx=0.01, rely=0.1)
            self.__currComponents.append(given)
            self.__currComponents.append(decision)
        if 'time' in self.__known and 'max_height' in self.__known:  # ИСПРАВИТЬ!!!!!!!!!!!!!!!!!!
            H = float(self.__data['max_height'])
            tf = float(self.__data['time'])
            v0 = find_v0_from_tf(tf, H)
            h = find_h(v0, tf)
            given = Label(text='Дано:\n'
                               'tf' + str(tf) + '\n'
                               'H=' + str(H) + '\n'
                               'Решение:', font='arial 12', anchor='e')
            given.place(relx=0.01, rely=0.01)
            s = "Высота броска h находится из кинематического уравнения по оси Y в момент времени tпол:\n" \
                "y(tпол) = h + v0*t - g*t*t/2 = 0 => h = g*t*t/2 - v0*t. Теперь найдем максимальную высоту подъема H:\n" \
                "H = y(tпод) = h + V0*tпод - g*t^2/2, где tпод - время подъема на высоту H\n" \
                "Vy(tпод) = V0 - g*tпод => tпод = v0/g. Подставим в предыдущее уравнение: \n" \
                "H = h + V0^2/2g. Подставим в эту формулу h: H = g*t^2/2 - V0*t + V0^2/2g\n" \
                "Решаем квадратное уравнение относительно v0 и получаем, что\n" \
                "v0 = 2*g*t + (2*g*H)^0.5 = " + format(v0, acc) + "\n" \
                "Подставляем v0: h=" + format(h, acc)

            decision = Label(text=s, font='arial 12', anchor='e')
            decision.place(relx=0.01, rely=0.1)
            self.__currComponents.append(given)
            self.__currComponents.append(decision)

    def __throw_error(self, s):
        showerror("Ошибка в условии", s)

    def __nextWindow(self):
        self.__currWindow += 1
        self.__setWindow()

    def __prevWindow(self):
        self.__data = dict()
        self.__unknown = dict()
        self.__known = dict()
        self.__currWindow -= 1
        self.__setWindow()

    def __setWindow(self):
        for c in self.__currComponents:
            c.place_forget()
        self.__currComponents = list()
        if self.__currWindow == 1:
            self.__setWindow1()
        elif self.__currWindow == 2:
            self.__setWindow2()
        else:
            self.__findKnown()
            self.__setWindow3()

    def __findKnown(self):
        for k in self.__data:
            self.__data[k] = self.__data[k].get()
        for k in self.__data:
            if self.__data[k] == '':
                self.__unknown[k] = self.__data[k]
            else:
                self.__known[k] = self.__data[k]

    def mainloop(self):
        self.__window.mainloop()


window = Window()
window.mainloop()
