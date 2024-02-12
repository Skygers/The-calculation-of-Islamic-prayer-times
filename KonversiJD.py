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