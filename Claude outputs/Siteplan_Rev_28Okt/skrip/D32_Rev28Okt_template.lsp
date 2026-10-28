;;; D32_Rev28Okt.lsp - Revisi Site Plan 28 Okt ke DWG Rev 24 Okt final
;;; Perintah: D32REV28
;;; 1. Buka SitePlan_Kroya_Smart_Unified_Market_Rev_24Okt_final.dwg
;;; 2. Seret file ini ke jendela AutoCAD (atau APPLOAD), ketik D32REV28
;;; Hasil: SitePlan_Kroya_Smart_Unified_Market_Rev28Okt.dwg (DWG 2018) di folder Siteplan_Rev_28Okt
;;; - model: jalan permukiman, Taman RT A/B, garis potong, nomor (UTM 49S, sisip 0,0 skala 1)
;;; - bangunan yang tertabrak jalan / di lahan Taman RT A dihapus dari DWG
;;; - layout SITEPLAN_A0_1-1000: tambahan legenda & keterangan kop
;;; - layout baru PNP_A ... PNP_D: penampang jalan A3 1:100
(vl-load-com)

;; jejak bangunan dihapus + buffer 2 m (UTM 49S = koordinat model DWG)
(setq *d32-hapus* '(
;;@@POLIGON_HAPUS@@
))

(setq *d32-layout-kop* "SITEPLAN_A0_1-1000")
;; sudut kiri-bawah teks "LEGENDA" pada kop Rev 24 Okt (mm kertas A0), acuan geser kop
(setq *d32-legenda-ll* '(743.05 192.15))
(setq *d32-pnp-layout* "PNP_A_BETET,PNP_B1_CENDRAWASIH,PNP_B2_CENDRAWASIH,PNP_C_LETKOL_SUDARSO,PNP_D_AMPAS_WARAS")

(defun d32:doc () (vla-get-activedocument (vlax-get-acad-object)))

(defun d32:cari-file (nama / dirs hasil)
  (setq dirs (list (strcat (getvar "DWGPREFIX") "..\\Siteplan_Rev_28Okt\\dxf\\")
                   (strcat (getvar "DWGPREFIX") "Siteplan_Rev_28Okt\\dxf\\")
                   (strcat (getvar "DWGPREFIX") "dxf\\")
                   (getvar "DWGPREFIX")))
  (foreach d dirs
    (foreach ext '(".dwg" ".dxf")
      (if (and (not hasil) (findfile (strcat d nama ext)))
        (setq hasil (findfile (strcat d nama ext))))))
  (if (not hasil)
    (setq hasil (getfiled (strcat "Pilih file " nama) (getvar "DWGPREFIX") "dxf;dwg" 0)))
  hasil)

;; sisipkan file sebagai block lalu explode di ruang aktif; T bila berhasil
(defun d32:sisip (blk file pt / e0 e ed obj)
  (if (tblsearch "BLOCK" blk) (command "_.-PURGE" "_B" blk "_N"))
  (setq e0 (entlast))
  (command "_.-INSERT" (strcat blk "=" file))
  (if (> (getvar "CMDACTIVE") 0) (command pt 1 1 0))
  (while (> (getvar "CMDACTIVE") 0) (command ""))
  (setq e (entlast))
  (if (and e (not (equal e e0))
           (setq ed (entget e))
           (= (cdr (assoc 0 ed)) "INSERT")
           (= (strcase (cdr (assoc 2 ed))) (strcase blk)))
    (progn
      (setq obj (vlax-ename->vla-object e))
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

(defun c:D32REV28 ( / *error* sv f-model f-kop f-pnp n geser dirout out lay ss pesan)
  (defun *error* (msg)
    (while (> (getvar "CMDACTIVE") 0) (command))
    (d32:pulih sv)
    (if (not (wcmatch (strcase msg) "*CANCEL*,*QUIT*,*BATAL*")) (princ (strcat "\nGalat: " msg)))
    (princ))
  (setq sv (mapcar '(lambda (v) (cons v (getvar v))) '("CMDECHO" "OSMODE" "FILEDIA" "EXPERT")))
  (setvar "CMDECHO" 0) (setvar "OSMODE" 0) (setvar "FILEDIA" 0) (setvar "EXPERT" 5)
  (setq pesan "")
  (if (ssget "_X" '((8 . "D32_JLN_ASPAL") (410 . "Model")))
    (progn
      (alert "Revisi 28 Okt sudah ada di gambar ini (layer D32_JLN_ASPAL).\nBuka kembali DWG Rev 24 Okt final lalu jalankan D32REV28 lagi.")
      (exit)))
  (setq f-model (d32:cari-file "D32_Overlay_Model_Rev28Okt_UTM49S")
        f-kop   (d32:cari-file "D32_Overlay_KopA0_Rev28Okt_mm")
        f-pnp   (d32:cari-file "D32_Penampang_Jalan_Permukiman_Rev28Okt"))
  (if (not (and f-model f-kop f-pnp)) (progn (alert "File overlay tidak ditemukan.") (exit)))

  ;; 1. model: overlay jalan + taman
  (setvar "TILEMODE" 1)
  (if (not (d32:sisip "D32_OVL_MODEL" f-model '(0.0 0.0 0.0)))
    (progn
      (alert (strcat "Gagal menyisipkan:\n" f-model
                     "\n\nBuka DXF tersebut, SAVEAS DWG ke folder yang sama (nama sama), lalu jalankan D32REV28 lagi."))
      (exit)))

  ;; 2. hapus bangunan yang tertabrak jalan / di lahan Taman RT A
  (setq n (d32:hapus-bangunan))
  (setq pesan (strcat pesan "\n- Objek bangunan/bayangan dihapus: " (itoa n)))
  (setq lay (vla-item (vla-get-layers (d32:doc)) "D32_BANGUNAN_DIHAPUS"))
  (vla-put-plottable lay :vlax-false)
  (vla-put-layeron lay :vlax-false)

  ;; 3. revisi di atas gambar lama
  (if (setq ss (ssget "_X" '((8 . "D32_*") (410 . "Model"))))
    (command "_.DRAWORDER" ss "" "_F"))

  ;; 4. penampang: geometri model (sekitar 0,0) + 5 layout A3
  (if (d32:sisip "D32_OVL_PNP" f-pnp '(0.0 0.0 0.0))
    (progn
      (command "_.-LAYOUT" "_T" f-pnp)
      (if (> (getvar "CMDACTIVE") 0) (command *d32-pnp-layout*))
      (while (> (getvar "CMDACTIVE") 0) (command ""))
      (setq pesan (strcat pesan "\n- Layout penampang: "
                          (if (member "PNP_A_BETET" (layoutlist)) "5 layout PNP_* ditambahkan"
                              "GAGAL impor layout (pakai LAYOUT > From Template > file penampang)"))))
    (setq pesan (strcat pesan "\n- Penampang: GAGAL sisip " f-pnp)))
  (command "_.ZOOM" "_W" '(305990.0 9156090.0) '(307070.0 9156600.0))

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

  ;; 6. simpan sebagai DWG baru (file Rev 24 Okt tidak diubah)
  (setq dirout (strcat (getvar "DWGPREFIX") "..\\Siteplan_Rev_28Okt\\"))
  (if (not (vl-file-directory-p dirout)) (setq dirout (getvar "DWGPREFIX")))
  (setq out (strcat dirout "SitePlan_Kroya_Smart_Unified_Market_Rev28Okt.dwg"))
  (if (and (findfile out) (not (vl-file-delete out)))
    (setq out (strcat dirout "SitePlan_Kroya_Smart_Unified_Market_Rev28Okt_"
                      (vl-string-subst "_" "." (rtos (getvar "CDATE") 2 4)) ".dwg")))
  (command "_.SAVEAS" "2018" out)
  (while (> (getvar "CMDACTIVE") 0) (command ""))
  (d32:pulih sv)
  (alert (strcat "Revisi 28 Okt selesai." pesan "\n\nTersimpan: " (getvar "DWGPREFIX") (getvar "DWGNAME")))
  (princ))

(princ "\nD32_Rev28Okt dimuat. Ketik D32REV28 untuk menerapkan revisi 28 Okt.")
(princ)
