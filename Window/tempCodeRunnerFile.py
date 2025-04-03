    self.model = QStandardItemModel()
        headers = ["NO", "NAMA", "POLI", "JENIS LAYANAN", "TANGGAL", "NO. ANTRIAN", "STATUS", "AKSI"]
        self.model.setHorizontalHeaderLabels(headers)
        self.tableView.setModel(self.model)
        
        # Hilangkan pengaturan fixed width kolom yang lama jika tidak dibutuhkan lagi
        # for i, width in enumerate(column_widths):
        #     self.tableView.setColumnWidth(i, width)
        
        # Atur tinggi baris
        self.tableView.verticalHeader().setDefaultSectionSize(45)
        
        # Set header font agar sama dengan WindowRiwayat
        header_font = QtGui.QFont("Garet", 12, QtGui.QFont.Bold)
        self.tableView.horizontalHeader().setFont(header_font)
        
        # Ubah mode resize kolom agar sesuai dengan isi konten masing-masing kolom
        for col in range(self.model.columnCount()):
            self.tableView.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.ResizeToContents)