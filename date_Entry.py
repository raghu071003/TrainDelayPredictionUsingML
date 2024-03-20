# uncompyle6 version 3.9.0
# Python bytecode version base 3.6 (3379)
# Decompiled from: Python 3.8.1 (tags/v3.8.1:1b293b6, Dec 18 2019, 23:11:46) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/niltech/Downloads/train delay/date_Entry.py
# Compiled at: 2019-01-01 23:59:38
# Size of source mod 2**32: 8929 bytes
"""
Simple calendar using ttk Treeview together with calendar and datetime
classes.
"""
import calendar, tkinter as Tkinter, tkinter.font as tkFont
from tkinter import ttk

def get_calendar(locale, fwday):
    if locale is None:
        return calendar.TextCalendar(fwday)
    else:
        return calendar.LocaleTextCalendar(fwday, locale)


class Calendar(ttk.Frame):
    datetime = calendar.datetime.datetime
    timedelta = calendar.datetime.timedelta

    def __init__(self, parent, master=None, **kw):
        """
        WIDGET-SPECIFIC OPTIONS

            locale, firstweekday, year, month, selectbackground,
            selectforeground
        """
        fwday = kw.pop('firstweekday', calendar.MONDAY)
        year = kw.pop('year', self.datetime.now().year)
        month = kw.pop('month', self.datetime.now().month)
        locale = kw.pop('locale', None)
        sel_bg = kw.pop('selectbackground', '#ecffc4')
        sel_fg = kw.pop('selectforeground', '#05640e')
        self._date = self.datetime(year, month, 1)
        self._selection = None
        self.parent = parent
        (ttk.Frame.__init__)(self, master, **kw)
        self._cal = get_calendar(locale, fwday)
        self._Calendar__setup_styles()
        self._Calendar__place_widgets()
        self._Calendar__config_calendar()
        self._Calendar__setup_selection(sel_bg, sel_fg)
        self._items = [self._calendar.insert('', 'end', values='') for _ in range(6)]
        self._build_calendar()
        self._calendar.bind('<Map>', self._Calendar__minsize)

    def proceed_fun(self):
        if self._selection:
            year, month = self._date.year, int(self._date.month)
            date = [int(self._selection[0]), month, year]
            self.responseB.configure(text=f"{date[0]}-{date[1]}-{date[2]}")
            self.parent.response['date'] = date
        self.pack_forget()
        self.parent.pack()

    def __setitem__(self, item, value):
        if item in ('year', 'month'):
            raise AttributeError("attribute '%s' is not writeable" % item)
        else:
            if item == 'selectbackground':
                self._canvas['background'] = value
            else:
                if item == 'selectforeground':
                    self._canvas.itemconfigure((self._canvas.text), item=value)
                else:
                    ttk.Frame.__setitem__(self, item, value)

    def __getitem__(self, item):
        if item in ('year', 'month'):
            return getattr(self._date, item)
        else:
            if item == 'selectbackground':
                return self._canvas['background']
            if item == 'selectforeground':
                return self._canvas.itemcget(self._canvas.text, 'fill')
            r = ttk.tclobjs_to_py({item: ttk.Frame.__getitem__(self, item)})
            return r[item]

    def __setup_styles(self):
        style = ttk.Style(self.master)
        arrow_layout = lambda dir: [
         (
          'Button.focus', {'children': [('Button.%sarrow' % dir, None)]})]
        style.layout('L.TButton', arrow_layout('left'))
        style.layout('R.TButton', arrow_layout('right'))

    def __place_widgets(self):
        proceedB = ttk.Button(self, text='Proceed', command=(self.proceed_fun))
        proceedB.pack(padx=10, pady=3)
        hframe = ttk.Frame(self)
        lbtn = ttk.Button(hframe, style='L.TButton', command=(self._prev_month))
        rbtn = ttk.Button(hframe, style='R.TButton', command=(self._next_month))
        self._header = ttk.Label(hframe, width=15, anchor='center')
        self._calendar = ttk.Treeview(show='', selectmode='none', height=7)
        hframe.pack(in_=self, side='top', pady=4, anchor='center')
        lbtn.grid(in_=hframe)
        self._header.grid(in_=hframe, column=1, row=0, padx=12)
        rbtn.grid(in_=hframe, column=2, row=0)
        self._calendar.pack(in_=self, expand=1, fill='both', side='bottom')

    def __config_calendar(self):
        cols = self._cal.formatweekheader(3).split()
        self._calendar['columns'] = cols
        self._calendar.tag_configure('header', background='grey90')
        self._calendar.insert('', 'end', values=cols, tag='header')
        font = tkFont.Font()
        maxwidth = max(font.measure(col) for col in cols)
        for col in cols:
            self._calendar.column(col, width=maxwidth, minwidth=maxwidth, anchor='e')

    def __setup_selection(self, sel_bg, sel_fg):
        self._font = tkFont.Font()
        self._canvas = canvas = Tkinter.Canvas((self._calendar), background=sel_bg,
          borderwidth=0,
          highlightthickness=0)
        canvas.text = canvas.create_text(0, 0, fill=sel_fg, anchor='w')
        canvas.bind('<ButtonPress-1>', (lambda evt: canvas.place_forget()))
        self._calendar.bind('<Configure>', (lambda evt: canvas.place_forget()))
        self._calendar.bind('<ButtonPress-1>', self._pressed)

    def __minsize(self, evt):
        width, height = self._calendar.master.geometry().split('x')
        height = height[:height.index('+')]
        self._calendar.master.minsize(width, height)

    def _build_calendar(self):
        year, month = self._date.year, self._date.month
        header = self._cal.formatmonthname(year, month, 0)
        self._header['text'] = header.title()
        cal = self._cal.monthdayscalendar(year, month)
        for indx, item in enumerate(self._items):
            week = cal[indx] if indx < len(cal) else []
            fmt_week = ['%02d' % day if day else '' for day in week]
            self._calendar.item(item, values=fmt_week)

    def _show_selection(self, text, bbox):
        """Configure canvas for a new selection."""
        x, y, width, height = bbox
        textw = self._font.measure(text)
        canvas = self._canvas
        canvas.configure(width=width, height=height)
        canvas.coords(canvas.text, width - textw, height / 2 - 1)
        canvas.itemconfigure((canvas.text), text=text)
        canvas.place(in_=(self._calendar), x=x, y=y)

    def _pressed(self, evt):
        """Clicked somewhere in the calendar."""
        x, y, widget = evt.x, evt.y, evt.widget
        item = widget.identify_row(y)
        column = widget.identify_column(x)
        if not column or item not in self._items:
            return
        item_values = widget.item(item)['values']
        if not len(item_values):
            return
        text = item_values[int(column[1]) - 1]
        if not text:
            return
        bbox = widget.bbox(item, column)
        if not bbox:
            return
        text = '%02d' % text
        self._selection = (text, item, column)
        self._show_selection(text, bbox)

    def _prev_month(self):
        """Updated calendar to show the previous month."""
        self._selection = None
        self._canvas.place_forget()
        self._date = self._date - self.timedelta(days=1)
        self._date = self.datetime(self._date.year, self._date.month, 1)
        self._build_calendar()

    def _next_month(self):
        """Update calendar to show the next month."""
        self._selection = None
        self._canvas.place_forget()
        year, month = self._date.year, self._date.month
        self._date = self._date + self.timedelta(days=(calendar.monthrange(year, month)[1] + 1))
        self._date = self.datetime(self._date.year, self._date.month, 1)
        self._build_calendar()

    @property
    def selection(self):
        """Return a datetime representing the current selected date."""
        if not self._selection:
            return
        else:
            year, month = self._date.year, self._date.month
            return self.datetime(year, month, int(self._selection[0]))


def test():
    import sys
    root = Tkinter.Tk()
    root.title('Ttk Calendar')
    parent = ttk.Frame(root)  # Create a parent frame within the root window
    ttkcal = Calendar(parent, firstweekday=(calendar.SUNDAY))
    ttkcal.pack(expand=1, fill='both')
    root.mainloop()


if __name__ == '__main__':
    test()
