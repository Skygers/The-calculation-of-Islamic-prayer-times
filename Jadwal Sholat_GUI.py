from tkinter import *
import tkinter.ttk as ttk
from tkinter.font import Font 
import pandas as pd 
from tkcalendar import Calendar, DateEntry
import calendar, datetime 
from time import strftime
import numpy as np
from tkinter import scrolledtext, Scrollbar
import sys
import os

class JDKeMasehi:


	def __init__(self, JD):
		self.JD = JD
		self.tahun = 0
		self.bulan = 0
		self.tanggal = 0

	def hitung_variabel(self):
		JD1 = self.JD + 0.5
		Z = int(JD1)
		F = JD1 - Z

		if Z == 229916:
			A = Z
		else:
			AA = int((Z - 1867216.25)/36524.25)
			A = Z + 1 + AA - int(AA/4)

		B = A + 1524
		C = int((B - 122.1)/365.25)
		D = int(365.25*C)
		E = int((B-D)/30.6001)

		return B, C, D, E, F

	def hitung_waktu(self, waktu):

		jam = int(waktu*24)
		menit = int(((waktu*24) - jam)*60)
		detik = int(((((waktu*24) - jam)*60)-menit)*60)

		return int(jam), int(menit), int(detik)

	def konversi_ke_masehi(self):

		B, C, D, E, F = self.hitung_variabel()

		self.tanggal = B - D - int(30.6001*E)

		if E == 14 or E == 15:
			self.bulan = E - 13

		elif E < 14:
			self.bulan = E - 1

		if self.bulan == 1 or self.bulan == 2:
			self.tahun = C - 4715
		elif self.bulan > 2:
			self.tahun = C-4716

		jam, menit, detik = self.hitung_waktu(F)

		hasil = "{}/{}/{}   {}:{}:{}".format(self.tahun, self.bulan, self.tanggal, jam, menit, detik)

		return hasil


class MasehiKeJD:

	def __init__(self, tahun, bulan, tanggal):
		self.tahun = tahun
		self.bulan = bulan
		self.tanggal = tanggal
		self.Gregorian = True

	def isGregorian(self):

		if self.tanggal < 15:
			if self.bulan < 10:
				if self.tahun <= 1582:
					self.Gregorian == False
				else:
					self.Gregorian == True

		return self.Gregorian

	def hitung_JD(self, Y, M, D):

		if self.isGregorian() == True:
			A = int(Y/100)
			B = 2 + int(A/4) - A

		elif self.isGregorian() == False:
			B = 0

		JD = 1720994.5 + int(365.25*Y) + int(30.6001*(M+1) + B + D)
		return JD

	def isLeap(self):
		kabisat = False
		if self.tahun % 4 == 0:
			if self.tahun % 100 == 0:
				if self.tahun % 400 == 0:
					kabisat = True
				else:
					kabisat = False
			else:
				kabisat = True
		else:
			kabisat = False

		return kabisat 

	def hari_dalam_bulan(self):
		tanggal = []
		if self.bulan in [4, 6, 9, 11]:
			tanggal = np.arange(1,31)
		elif self.bulan == 1:
			tanggal = np.arange(1,32)
		elif self.bulan == 2:
			if self.isLeap():
				tanggal = np.arange(1,30)
			else:
				tanggal = np.arange(1,29)
		elif self.bulan in [3, 5, 7, 8, 10, 12]:
			tanggal = np.arange(1,32)
		else:
			tanggal = [0]

		return tanggal

	def konversi_ke_JD(self):

		if self.tahun >= -4712:

			julian_day = 0

			if self.tahun == 1582 and self.bulan == 10:
				if self.tanggal in np.arange(5,15):
					julian_day = 'Tanggal tidak tersedia'
				else:
					julian_day = self.hitung_JD(self.tahun, self.bulan, self.tanggal)

			elif self.bulan <= 2:
				hari = self.hari_dalam_bulan()
				if self.tanggal in hari:
					self.bulan = self.bulan + 12
					self.tahun = self.tahun -1
					julian_day = self.hitung_JD(self.tahun, self.bulan, self.tanggal)
				else:
					julian_day = 'Tanggal tidak tersedia'

			elif self.bulan > 12:
				julian_day = 'Bulan tidak teredia'

			else:
				self.bulan = self.bulan
				self.tahun = self.tahun

				hari = self.hari_dalam_bulan()
				if self.tanggal in hari:
					julian_day = self.hitung_JD(self.tahun, self.bulan, self.tanggal)
				else:
					julian_day = 'Tanggal tidak tersedia'

		else:
			julian_day = 'Tahun tidak tersedia'

		return julian_day





class WaktuSholat:
	
	def __init__(self, tahun, bulan, tanggal, lintang, bujur, zona_waktu, ketinggian = 25, jam = 12):
		self.tahun = tahun
		self.bulan = bulan 
		self.tanggal = tanggal
		self.lintang = lintang
		self.bujur = bujur
		self.zona_waktu = zona_waktu
		self.jam = jam
		self.ketinggian = ketinggian

	def sudut_tanggal(self):

		julian_day = MasehiKeJD(self.tahun, self.bulan, self.tanggal)
		JD = (julian_day.konversi_ke_JD() + self.jam/24) - self.zona_waktu/24
		T = 2*np.pi*(JD - 2451545)/365.25
		return T, JD

	def deklinasi_matahari(self):

		T, JD = self.sudut_tanggal()
		delta = (0.37877 + 23.264*np.sin(np.deg2rad(57.297*T - 79.547)) + 
				 0.3812*np.sin(np.deg2rad(2*57.297*T - 82.682)) + 
				 0.17132 * np.sin(np.deg2rad(3*57.927 * T - 59.722)))
		return delta

	def equation_of_time(self):
		
		T, JD = self.sudut_tanggal()
		U = (JD - 2451545)/36525
		L0 = 280.46607 + 36000.7698*U
		ET = (-(1789+237*U)*np.sin(np.deg2rad(L0)) - 
			 (7146-62*U)*np.cos(np.deg2rad(L0)) + 
			 (9934-14*U)*np.sin(np.deg2rad(2*L0)) - 
			 (29+5*U)*np.cos(np.deg2rad(2*L0)) + 
			 (74+10*U)*np.sin(np.deg2rad(3*L0)) + 
			 (320 - 4*U)*np.cos(np.deg2rad(3*L0)) - 
			 212*np.sin(np.deg2rad(4*L0)))/1000
		return ET

	def waktu_transit(self):
		
		ET = self.equation_of_time()
		transit = 12 + self.zona_waktu - self.bujur/15 - ET/60
		return transit

	def hour_angle(self, altitude, delta):
		
		hour_angle = (np.sin(np.deg2rad(altitude)) - 
					 np.sin(np.deg2rad(self.lintang)) * 
					 np.sin(np.deg2rad(delta))) / (np.cos(np.deg2rad(self.lintang)) *
					 np.cos(np.deg2rad(delta)))

		HA = np.arccos(hour_angle)
	
		return np.degrees(HA)

	def zuhur(self):
		
		transit = self.waktu_transit()
		zuhur = transit + 2/60
		return zuhur

	def ashar(self):
		
		transit = self.waktu_transit()
		delta = self.deklinasi_matahari()
		KA = 1
		altitude_1 = np.tan(np.deg2rad(np.abs(delta - self.lintang)))
		altitude = np.arctan(1/(KA + altitude_1 ))
		HA = self.hour_angle(np.degrees(altitude), delta)
		ashar = transit + HA/15
		return ashar

	def maghrib(self):
		
		transit = self.waktu_transit()
		delta = self.deklinasi_matahari()
		altitude = -0.8333 - 0.0347*np.sqrt(self.ketinggian)
		HA = self.hour_angle(altitude, delta)
		maghrib = transit + HA/15
		return maghrib

	def isya(self):
		
		transit = self.waktu_transit()
		delta = self.deklinasi_matahari()
		altitude = -18
		HA = self.hour_angle(altitude, delta)
		isya = transit + HA/15
		return isya

	def subuh(self):
		
		transit = self.waktu_transit()
		delta = self.deklinasi_matahari()
		altitude = -20
		HA = self.hour_angle(altitude, delta)
		subuh = transit - HA/15
		return subuh

	def terbit(self):
		
		transit = self.waktu_transit()
		delta = self.deklinasi_matahari()
		altitude = -0.8333 - 0.0347*np.sqrt(self.ketinggian)
		HA = self.hour_angle(altitude, delta)
		terbit = transit - HA/15
		return terbit

	def ubah_ke_jam(self, waktu):
		
		pukul = int(waktu)
		menit = int((waktu - pukul)*60)
		detik = int((((waktu - pukul)*60) - menit )*60)

		if pukul<10:
			pukul = '0'+str(abs(pukul))
		if menit<10:
			menit = '0'+str(abs(menit))
		if detik<10:
			detik = '0'+str(abs(detik))
		hasil = '{}:{}:{}'.format(pukul, menit, detik)
		return hasil

	def show_result(self):
		
		
		subuh = self.ubah_ke_jam(self.subuh())
		terbit = self.ubah_ke_jam(self.terbit())
		zuhur = self.ubah_ke_jam(self.zuhur())
		ashar = self.ubah_ke_jam(self.ashar())
		maghrib = self.ubah_ke_jam(self.maghrib())
		isya = self.ubah_ke_jam(self.isya())
		

		return subuh, terbit, zuhur, ashar, maghrib, isya



class Window:

	def __init__(self, master):

		self.master = master
		self.init_window()
		
	def init_window(self):

		self.master.title("Jadwal Waktu Sholat")
		self.fontstyle = Font(family='Times New Roman', size=12)
		self.fontstyle2 = Font(family='Calibri', size=11)
		self.fontstyle3 = ('Times New Roman', 12, 'bold')
		self.fontstyle4 = ('Times New Roman', 17, 'bold')
		self.membuat_frame() 
		self.get_date()
		self.frame_1()
		self.convert_button()
		self.frame_3()
		
	def membuat_frame(self):

		self.frame1 = Frame(height=210, width=925, bg='#ded95b', borderwidth=3, )
		self.frame2 = Frame(height=210, width=360, bg='#ded95b', borderwidth=3, )
		self.frame3 = Frame(height=390, width=925, bg='#ded95b', borderwidth=3, )
		self.frame3.place(x=10, y=10)
		self.frame2.place(x=575, y=10)
		self.frame1.place(x=10, y=415)

	def get_date(self):

		self.kalender = Calendar(self.frame1, font=self.fontstyle2, selectmode='day', cursor='hand1')
		self.kalender.place(x=260, y=0)
		selected_date=None

	
	def dataset(self):

		dataset = pd.read_csv(os.path.dirname(os.getcwd())+'/Pandu Hafizh Ananta_195090307111015_Jadwal Sholat/Dataset.csv', sep=';')
		negara = dataset.Country
		negara = negara.drop_duplicates()

		return negara, dataset

	def frame_1(self): 

		title = Label(self.frame1, text="Masukkan Data Dibawah", font=(self.fontstyle), fg='Black', bg='#ded95b')
		title.place(x=75, y=5)
		style = ttk.Style()
		style.theme_use('clam')

		lbl_negara = Label(self.frame1, text='Negara 	    : ', font=self.fontstyle, bg='#ded95b')
		tanggal = Label(self.frame1, text='Tanggal 	    : ', font=self.fontstyle, bg='#ded95b')
		lbl_kota = Label(self.frame1, text='Kota    	    :', font=self.fontstyle, bg='#ded95b')
		lbl_tanggalVar = StringVar()
		lbl_tanggal = Label(self.frame1, text=self.kalender.selection_get(), font=self.fontstyle, width=15, justify='center', bg='#fff1a8')

		def select_date():

			date = self.kalender.selection_get()
			lbl_tanggal.configure(text=date)

		style.map('TCombobox', fieldbackground=[('readonly', '#fff1a8')])
		style.map('TCombobox', background=[('readonly', '#fff1a8')])
		style.map('TCombobox', foreground=[('readonly', 'Black')])
		cmb_negaraVar = StringVar()
		self.cmb_negara = ttk.Combobox(self.frame1, textvariable='cmb_negaraVar', font=self.fontstyle, width=15, justify='center')
		
		cmb_kotaVar = StringVar()
		self.cmb_kota = ttk.Combobox(self.frame1, textvariable='cmb_kotaVar', font=self.fontstyle, width=15, justify='center')
		
		negara, dataset = self.dataset()
		value_negara = ['Pilih Negara']
		for country in negara:
			value_negara.append(country)
		
		self.cmb_negara['values'] = value_negara
		self.cmb_negara['state'] = 'readonly'
		self.cmb_negara.current(0)

		#Place
		lbl_negara.place(x=5, y=32)
		tanggal.place(x=5, y=100)
		self.cmb_negara.place(x=100, y=32)
		lbl_tanggal.place(x=100, y=100)
		lbl_kota.place(x=5, y=68)
		self.cmb_kota.place(x=100, y=65)

	
	def take_city_value(self):

		negara, dataset = self.dataset()
		negara_pilih = self.cmb_negara.current()

		def callback(eventObject):
			
			pilihan_negara = eventObject.widget.get()
			print(eventObject.widget.get())
			negara_mask = dataset["Country"].values == pilihan_negara
			kota = dataset["City"].loc[negara_mask]

			self.value_kota = []
			for city in kota:
				self.value_kota.append(city)

			self.cmb_kota['values'] = self.value_kota
			self.cmb_kota['state'] = 'readonly'
			self.cmb_kota.current(0)

		self.cmb_negara.bind("<<ComboboxSelected>>", callback)

		kota_cmb = self.cmb_kota.get()
		negara_cmb = self.cmb_negara.get()
		print(kota_cmb)
		nama_kota = dataset.loc[dataset['City'] == kota_cmb]
		
		return nama_kota, kota_cmb, negara_cmb

	def hitung_waktu_shalat(self):
	
		nama_kota, kota_cmb, negara_cmb = self.take_city_value()
		
		try:
			lintang = float(nama_kota.Latitude.values[0])
			bujur = float(nama_kota.Longitude.values[0])
			ketinggian = nama_kota.Elevation.values[0]
			zona_waktu = nama_kota.Time_zone.values[0]
		except IndexError:	
			lintang =  0
			bujur = 0
			ketinggian = 50
			zona_waktu = 0
			
		tahun = self.kalender.selection_get().year
		bulan = self.kalender.selection_get().month
		tanggal = self.kalender.selection_get().day
	

		if int(zona_waktu) > 0:
			get_time_zone = '+'+str(zona_waktu)
		else:
			get_time_zone = str(zona_waktu)

		nama_bulanDict = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
		no_bulan = list(nama_bulanDict.keys())
		nama_bulan = list(nama_bulanDict.values())
		jumlah_hari = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

		sign_lat = 'N'
		if lintang < 0:
			sign_lat = 'S'

		sign_lng = 'E'
		if bujur < 0:
			sign_lng = 'W'

		
		def isLeap(tahun):

			kabisat = 28
			if tahun % 4 == 0:
				if tahun % 100 == 0:
					if tahun % 400 == 0:
						kabisat = 29
					else:
						kabisat = 28
				else:
					kabisat = 29
			else:
				kabisat = 28
			return kabisat

		if bulan == 2:
			jumlah_hari[1] = isLeap(tahun)

		month = []
		date = 0
		for i in range(0, len(no_bulan)+1):
			if bulan == no_bulan[i-1]:
				month.append(nama_bulan[i-1])
			if i == bulan:
				date = (jumlah_hari[i-1])
		
		subuh_list = []
		terbit_list = []
		zuhur_list = []
		ashar_list = []
		maghrib_list = []
		isya_list = []

		for day in range(1, int(date)+1):
			try:
				jadwal_shalat = WaktuSholat(tahun, bulan, day, lintang, bujur, zona_waktu, ketinggian)
				subuh, terbit, zuhur, ashar, maghrib, isya = jadwal_shalat.show_result()
				subuh_list.append(subuh)
				terbit_list.append(terbit)
				zuhur_list.append(zuhur)
				ashar_list.append(ashar)
				maghrib_list.append(maghrib)
				isya_list.append(isya)

			except ValueError:
				continue
			continue

		self.lbl_date = Label(self.frame3, text='{} {} {}'.format(tanggal, month[0], tahun), width=10, font=self.fontstyle3, bg='#fff1a8', justify="center", fg='black')
		self.lbl_date.place(x=770, y=35)

		return date, month, subuh_list, terbit_list, zuhur_list, ashar_list, maghrib_list, isya_list

	def convert_button(self):

		style = ttk.Style()
		style.configure('TButton', font=self.fontstyle2, bg='dark green', width=10)
		btn_convert = ttk.Button(self.frame1, text='Tekan disini', style='TButton', width=20, command=self.take_value)
		btn_convert.place(x=60, y=160)

	def take_value(self):

		date, month, subuh, terbit, zuhur, ashar, maghrib, isya = self.hitung_waktu_shalat()
		tanggal = self.kalender.selection_get().day
		self.scr_jadwal.delete(1.0, END)
		x_tanggal = 3
		x_subuh = x_tanggal+135
		x_terbit = x_subuh+135
		x_zuhur = x_subuh+135
		x_ashar = x_zuhur+135
		x_maghrib = x_ashar+135
		x_isya = x_maghrib+135
		y_size = 30

		for i in range(0, date):
			if i+1 < 10:
				self.scr_jadwal.state = NORMAL
				self.scr_jadwal.insert(END, '  0{} {}           \t{}         \t{}           \t{}          \t {}           \t  {}        \t  {}\n'.format(i+1, str(month[0]), subuh[i],
								terbit[i], zuhur[i], ashar[i], maghrib[i], isya[i]))
				self.scr_jadwal.state = DISABLED
			else:
				self.scr_jadwal.state = NORMAL
				self.scr_jadwal.insert(END, '  {} {}           \t{}         \t{}           \t{}          \t {}           \t  {}        \t  {}\n'.format(i+1, str(month[0]), subuh[i],
								terbit[i], zuhur[i], ashar[i], maghrib[i], isya[i]))
				self.scr_jadwal.state = DISABLED

			if tanggal == i+1:
				lbl_subuh = Label(self.frame3, text=subuh[i], font=self.fontstyle3, bg='#fff1a8', fg='black')
				lbl_terbit = Label(self.frame3, text=terbit[i], font=self.fontstyle3, bg='#fff1a8', fg='black')
				lbl_zuhur = Label(self.frame3, text=zuhur[i], font=self.fontstyle3, bg='#fff1a8', fg='black')
				lbl_ashar = Label(self.frame3, text=ashar[i], font=self.fontstyle3, bg='#fff1a8', fg='black')
				lbl_maghrib = Label(self.frame3, text=maghrib[i], font=self.fontstyle3, bg='#fff1a8', fg='black')
				lbl_isya = Label(self.frame3, text=isya[i], font=self.fontstyle3, bg='#fff1a8', fg='black')

				lbl_subuh.place(x=820, y=140)
				lbl_terbit.place(x=820, y=180)
				lbl_zuhur.place(x=820, y=220)
				lbl_ashar.place(x=820, y=260)
				lbl_maghrib.place(x=820, y=300)
				lbl_isya.place(x=820, y=340)

	def frame_3(self):
		'''Frame - 3'''

		tahun = self.kalender.selection_get().year
		bulan = self.kalender.selection_get().month
		tanggal = self.kalender.selection_get().day

		date, month, subuh, terbit, zuhur, ashar, maghrib, isya = self.hitung_waktu_shalat()
	
		lbl_index = Label(self.frame3, text='', bg='#fff1a8', font=self.fontstyle2, width='87')
		lbl_index.place(x=3, y=3)
		indexx = ['TANGGAL', 'SUBUH', 'TERBIT', 'ZUHUR', 'ASHAR', ' MAGHRIB', '   ISYA']
		x_size = 3
		y_size = 3
		
		for i in range(0, len(indexx)):
			lbl_tanggal = Label(self.frame3, text=indexx[i], font=self.fontstyle2, bg='#fff1a8')
			lbl_tanggal.place(x=x_size, y=y_size)
			x_size = x_size + 100

		self.scr_jadwal = scrolledtext.ScrolledText(self.frame3, width=85, height=18, bg='#fff1a8', font=self.fontstyle)
		self.scr_jadwal.place(x=5, y=30)

		lbl_jadwal = Label(self.frame3, text='JADWAL SHALAT', font=self.fontstyle3, bg='#fff1a8', fg='black')
		lbl_jadwal.place(x=750, y=15)

		x_size2 = 730
		y_size2 = 140
		index = ['SUBUH', 'TERBIT', 'ZUHUR', 'ASHAR', 'MAGHRIB', 'ISYA']
		for i in range(0, len(index)):
			lbl_subuh = Label(self.frame3, text=index[i], font=self.fontstyle, bg='#fff1a8', fg='black')
			lbl_subuh.place(x=x_size2, y=y_size2)
			y_size2 = y_size2+40

	
root = Tk()
app = Window(root)
root.geometry('950x650')
root.resizable(0,0)
root.mainloop()