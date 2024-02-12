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