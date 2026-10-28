;;; D32_Rev28Okt.lsp - Revisi Site Plan 28 Okt ke DWG Rev 24 Okt final  (v3)
;;; Perintah: D32REV28
;;; 1. Buka SitePlan_Kroya_Smart_Unified_Market_Rev_24Okt_final.dwg
;;;    (atau ..._Rev28Okt.dwg hasil percobaan sebelumnya: revisi lama dibersihkan lalu dipasang ulang)
;;; 2. Seret file ini ke jendela AutoCAD (atau APPLOAD), ketik D32REV28
;;; Hasil: SitePlan_Kroya_Smart_Unified_Market_Rev28Okt.dwg (DWG 2018)
;;; - model: jalan permukiman, Taman RT A/B, pohon, garis potong, nomor (UTM 49S, 0,0 skala 1)
;;; - bangunan yang tertabrak jalan / di lahan Taman RT A dihapus dari DWG
;;; - layout SITEPLAN_A0_1-1000: tambahan legenda & keterangan kop
;;; - layout PNP_A ... PNP_D: penampang jalan A3 1:100
(vl-load-com)

;; jejak bangunan dihapus + buffer 2 m (UTM 49S = koordinat model DWG)
(setq *d32-hapus* '(
;;@@POLIGON_HAPUS@@
))

(setq *d32-layout-kop* "SITEPLAN_A0_1-1000")
;; sudut kiri-bawah teks "LEGENDA" pada kop Rev 24 Okt (mm kertas A0), acuan geser kop
(setq *d32-legenda-ll* '(743.05 192.15))
(setq *d32-pnp-layout* "PNP_A_BETET,PNP_B1_CENDRAWASIH,PNP_B2_CENDRAWASIH,PNP_C_LETKOL_SUDARSO,PNP_D_AMPAS_WARAS")
(setq *d32-nama-hasil* "SitePlan_Kroya_Smart_Unified_Market_Rev28Okt")

(defun d32:doc () (vla-get-activedocument (vlax-get-acad-object)))

(setq *d32-dir* nil)
(defun d32:cari-file (nama / dirs hasil)
  (setq dirs (list (if *d32-dir* *d32-dir* (getvar "DWGPREFIX"))
                   (if *d32-dir* (strcat *d32-dir* "dxf\\") (getvar "DWGPREFIX"))
                   (strcat (getvar "DWGPREFIX") "dxf\\")
                   (strcat (getvar "DWGPREFIX") "..\\Siteplan_Rev_28Okt\\dxf\\")
                   (strcat (getvar "DWGPREFIX") "Siteplan_Rev_28Okt\\dxf\\")
                   (getvar "DWGPREFIX")))
  (foreach d dirs
    (foreach ext '(".dwg" ".dxf")
      (if (and (not hasil) (findfile (strcat d nama ext)))
        (setq hasil (findfile (strcat d nama ext))))))
  (if (not hasil)
    (progn
      (alert (strcat "Pilih file berikut di jendela berikutnya:\n\n   " nama ".dxf\n\n(ada di folder  dxf  hasil ekstrak ZIP)"))
      ;; ulangi sampai file yang dipilih benar atau dibatalkan
      (while (and (setq hasil (getfiled (strcat "Pilih " nama ".dxf")
                                        (if *d32-dir* *d32-dir* (getvar "DWGPREFIX")) "dxf;dwg" 0))
                  (/= (strcase (vl-filename-base hasil)) (strcase nama)))
        (alert (strcat "File yang dipilih salah:\n   " (vl-filename-base hasil)
                       "\n\nYang dibutuhkan:\n   " nama)))))
  ;; file berikutnya dicari di folder yang sama, jadi cukup pilih sekali
  (if hasil (setq *d32-dir* (strcat (vl-filename-directory hasil) "\\")))
  hasil)

;; sisipkan file sebagai block lalu explode di ruang aktif; T bila berhasil.
;; konversi unit dimatikan dan posisi/skala dipaksa, jadi koordinat UTM masuk 1:1.
(defun d32:sisip (blk file pt / e0 e ed obj su)
  (if (tblsearch "BLOCK" blk) (command "_.-PURGE" "_B" blk "_N"))
  (setq su (mapcar 'getvar '("INSUNITS" "INSUNITSDEFSOURCE" "INSUNITSDEFTARGET")))
  (setvar "INSUNITS" 0) (setvar "INSUNITSDEFSOURCE" 0) (setvar "INSUNITSDEFTARGET" 0)
  (setq e0 (entlast))
  (command "_.-INSERT" (strcat blk "=" file))
  (if (> (getvar "CMDACTIVE") 0) (command pt 1 1 0))
  (while (> (getvar "CMDACTIVE") 0) (command ""))
  (mapcar 'setvar '("INSUNITS" "INSUNITSDEFSOURCE" "INSUNITSDEFTARGET") su)
  (setq e (entlast))
  (if (and e (not (equal e e0))
           (setq ed (entget e))
           (= (cdr (assoc 0 ed)) "INSERT")
           (= (strcase (cdr (assoc 2 ed))) (strcase blk)))
    (progn
      (setq obj (vlax-ename->vla-object e))
      (vla-put-InsertionPoint obj (vlax-3d-point pt))
      (vla-put-XScaleFactor obj 1.0)
      (vla-put-YScaleFactor obj 1.0)
      (vla-put-ZScaleFactor obj 1.0)
      (vla-put-Rotation obj 0.0)
      (vla-explode obj)
      (vla-delete obj)
      (command "_.-PURGE" "_B" blk "_N")
      T)
    nil))

(defun d32:layer-kunci ( / r a l)
  (setq a T)
  (while (setq r (tblnext "LAYER" a))
    (setq a nil)
    (if (= 4 (logand 4 (cdr (assoc 70 r)))) (setq l (cons (cdr (assoc 2 r)) l))))
  l)

(defun d32:kunci (nama v)
  (vla-put-lock (vla-item (vla-get-layers (d32:doc)) nama) v))

;; hapus semua hasil percobaan sebelumnya (layer D32_* di semua ruang + layout PNP_*)
(defun d32:bersihkan ( / ss i n)
  (setq n 0)
  (foreach l (d32:layer-kunci) (if (wcmatch (strcase l) "D32_*") (d32:kunci l :vlax-false)))
  (if (setq ss (ssget "_X" '((8 . "D32_*"))))
    (progn
      (setq i 0 n (sslength ss))
      (repeat n (entdel (ssname ss i)) (setq i (1+ i)))))
  (setvar "CTAB" "Model")
  (foreach l (layoutlist)
    (if (wcmatch (strcase l) "PNP_*") (command "_.-LAYOUT" "_D" l)))
  n)

;; hapus bangunan (+ bayangan) yang seluruhnya berada di dalam poligon hapus
(defun d32:hapus-bangunan ( / kunci n ss pts xs ys)
  (setq kunci (d32:layer-kunci) n 0)
  (foreach l kunci (d32:kunci l :vlax-false))
  (foreach poly *d32-hapus*
    (setq pts (mapcar '(lambda (p) (list (car p) (cadr p) 0.0)) poly)
          xs (mapcar 'car pts)
          ys (mapcar 'cadr pts))
    (command "_.ZOOM" "_W"
             (list (- (apply 'min xs) 5.0) (- (apply 'min ys) 5.0))
             (list (+ (apply 'max xs) 5.0) (+ (apply 'max ys) 5.0)))
    (setq ss (ssget "_WP" pts
                    '((-4 . "<AND")
                        (8 . "*BANGU*,*BAYANG*,*RUMAH*,*GEDUNG*")
                        (-4 . "<NOT") (8 . "D32_*") (-4 . "NOT>")
                      (-4 . "AND>"))))
    (if ss
      (progn (setq n (+ n (sslength ss))) (command "_.ERASE" ss ""))))
  (foreach l kunci (d32:kunci l :vlax-true))
  n)

;; cek overlay site plan benar-benar ada di koordinat UTM tapak
(defun d32:cek-overlay ( / ss obj mn mx ll n)
  (setq n (if (setq ss (ssget "_X" '((8 . "D32_JLN_*,D32_RT_*") (410 . "Model")))) (sslength ss) 0))
  (if (setq ss (ssget "_X" '((8 . "D32_JLN_ASPAL") (410 . "Model"))))
    (progn
      (setq obj (vlax-ename->vla-object (ssname ss 0)))
      (vla-getboundingbox obj 'mn 'mx)
      (setq ll (vlax-safearray->list mn))
      (if (and (> (car ll) 305000.0) (< (car ll) 308000.0) (> (cadr ll) 9155000.0) (< (cadr ll) 9158000.0))
        (strcat "OK, " (itoa n) " objek jalan/taman di posisi tapak")
        (strcat "POSISI SALAH (" (rtos (car ll) 2 1) ", " (rtos (cadr ll) 2 1) ")")))
    "TIDAK MASUK"))

;; geser kop bila kertas layout tidak berawal di 0,0 (acuan teks LEGENDA)
(defun d32:geser-kop ( / ss obj mn mx ll dx dy)
  (setq dx 0.0 dy 0.0)
  (if (setq ss (ssget "_X" (list '(0 . "TEXT,MTEXT") '(1 . "*LEGENDA*") (cons 410 *d32-layout-kop*))))
    (progn
      (setq obj (vlax-ename->vla-object (ssname ss 0)))
      (vla-getboundingbox obj 'mn 'mx)
      (setq ll (vlax-safearray->list mn)
            dx (- (car ll) (car *d32-legenda-ll*))
            dy (- (cadr ll) (cadr *d32-legenda-ll*)))
      (if (and (< (abs dx) 4.0) (< (abs dy) 4.0)) (setq dx 0.0 dy 0.0))))
  (list dx dy 0.0))

(defun d32:pulih (sv) (foreach p sv (setvar (car p) (cdr p))))

(defun c:D32REV28 ( / *error* sv f-model f-kop f-pnp n geser dirout out lay ss pesan jwb cek)
  (defun *error* (msg)
    (while (> (getvar "CMDACTIVE") 0) (command))
    (d32:pulih sv)
    (if (not (wcmatch (strcase msg) "*CANCEL*,*QUIT*,*BATAL*")) (princ (strcat "\nGalat: " msg)))
    (princ))
  (setq sv (mapcar '(lambda (v) (cons v (getvar v))) '("CMDECHO" "OSMODE" "FILEDIA" "EXPERT")))
  (setq pesan "")

  ;; 0. revisi lama (percobaan sebelumnya) dibersihkan dulu
  (if (ssget "_X" '((8 . "D32_*")))
    (progn
      (initget "Ya Tidak")
      (setq jwb (getkword "\nRevisi 28 Okt lama ditemukan di gambar ini. Hapus dan pasang ulang? [Ya/Tidak] <Ya>: "))
      (if (= jwb "Tidak") (exit))))
  (setvar "CMDECHO" 0) (setvar "OSMODE" 0) (setvar "FILEDIA" 0) (setvar "EXPERT" 5)
  (setq n (d32:bersihkan))
  (if (> n 0) (setq pesan (strcat pesan "\n- Revisi lama dibersihkan: " (itoa n) " objek")))

  (setq f-model (d32:cari-file "D32_Overlay_Model_Rev28Okt_UTM49S"))
  (if f-model (setq f-kop (d32:cari-file "D32_Overlay_KopA0_Rev28Okt_mm")))
  (if f-kop (setq f-pnp (d32:cari-file "D32_Penampang_Jalan_Permukiman_Rev28Okt")))
  (if (not (and f-model f-kop f-pnp)) (progn (alert "File DXF revisi tidak lengkap, proses dibatalkan.") (exit)))

  ;; 1. model: overlay jalan + taman (UTM, 0,0 skala 1)
  (setvar "TILEMODE" 1)
  (if (not (d32:sisip "D32_OVL_MODEL" f-model '(0.0 0.0 0.0)))
    (progn
      (alert (strcat "Gagal menyisipkan:\n" f-model
                     "\n\nBuka DXF tersebut, SAVEAS DWG ke folder yang sama (nama sama), lalu jalankan D32REV28 lagi."))
      (exit)))
  (setq cek (d32:cek-overlay))
  (setq pesan (strcat pesan "\n- Overlay site plan: " cek))

  ;; 2. hapus bangunan yang tertabrak jalan / di lahan Taman RT A
  (setq n (d32:hapus-bangunan))
  (setq pesan (strcat pesan "\n- Objek bangunan/bayangan dihapus: " (itoa n)))
  (if (tblsearch "LAYER" "D32_BANGUNAN_DIHAPUS")
    (progn
      (setq lay (vla-item (vla-get-layers (d32:doc)) "D32_BANGUNAN_DIHAPUS"))
      (vla-put-plottable lay :vlax-false)
      (vla-put-layeron lay :vlax-false)))

  ;; 3. revisi di atas gambar lama
  (if (setq ss (ssget "_X" '((8 . "D32_*") (410 . "Model"))))
    (command "_.DRAWORDER" ss "" "_F"))

  ;; 4. penampang: geometri model (sekitar 0,0, jauh dari tapak) + 5 layout A3
  (if (d32:sisip "D32_OVL_PNP" f-pnp '(0.0 0.0 0.0))
    (progn
      (command "_.-LAYOUT" "_T" f-pnp)
      (if (> (getvar "CMDACTIVE") 0) (command *d32-pnp-layout*))
      (while (> (getvar "CMDACTIVE") 0) (command ""))
      (setq pesan (strcat pesan "\n- Layout penampang: "
                          (if (member "PNP_A_BETET" (layoutlist)) "5 layout PNP_* ditambahkan"
                              "GAGAL impor layout (pakai LAYOUT > From Template > file penampang)"))))
    (setq pesan (strcat pesan "\n- Penampang: GAGAL sisip " f-pnp)))

  ;; 5. kop: tambahan legenda & keterangan di layout SITEPLAN_A0_1-1000
  (if (member *d32-layout-kop* (layoutlist))
    (progn
      (setvar "CTAB" *d32-layout-kop*)
      (command "_.PSPACE")
      (setq geser (d32:geser-kop))
      (if (d32:sisip "D32_OVL_KOP" f-kop geser)
        (setq pesan (strcat pesan "\n- Kop ditambahkan di " *d32-layout-kop*
                            " (geser " (rtos (car geser) 2 1) ", " (rtos (cadr geser) 2 1) " mm)"))
        (setq pesan (strcat pesan "\n- Kop: GAGAL sisip " f-kop)))
      (command "_.ZOOM" "_E"))
    (setq pesan (strcat pesan "\n- Layout " *d32-layout-kop* " tidak ada, kop tidak disisipkan")))

  ;; 6. tampilkan model di tapak, lalu simpan sebagai DWG Rev 28 Okt (file Rev 24 Okt tidak diubah)
  (setvar "CTAB" "Model")
  (command "_.ZOOM" "_W" '(305990.0 9156090.0) '(307070.0 9156600.0))
  (if (= (strcase (vl-filename-base (getvar "DWGNAME"))) (strcase *d32-nama-hasil*))
    (command "_.QSAVE")
    (progn
      (setq dirout (strcat (getvar "DWGPREFIX") "..\\Siteplan_Rev_28Okt\\"))
      (if (not (vl-file-directory-p dirout)) (setq dirout (getvar "DWGPREFIX")))
      (setq out (strcat dirout *d32-nama-hasil* ".dwg"))
      (if (and (findfile out) (not (vl-file-delete out)))
        (setq out (strcat dirout *d32-nama-hasil* "_"
                          (vl-string-subst "_" "." (rtos (getvar "CDATE") 2 4)) ".dwg")))
      (command "_.SAVEAS" "2018" out)))
  (while (> (getvar "CMDACTIVE") 0) (command ""))
  (d32:pulih sv)
  (alert (strcat "Revisi 28 Okt selesai." pesan "\n\nTersimpan: " (getvar "DWGPREFIX") (getvar "DWGNAME")))
  (princ))

(princ "\nD32_Rev28Okt v3 dimuat. Ketik D32REV28 untuk menerapkan revisi 28 Okt.")
(princ)
