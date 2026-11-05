from pathlib import Path
from html import escape
from PIL import Image, ImageDraw, ImageFont
import math

OUT = Path(__file__).parent / 'assets'
OUT.mkdir(exist_ok=True)
REG = 'C:/Windows/Fonts/segoeui.ttf'
BOLD = 'C:/Windows/Fonts/seguisb.ttf'
INK = '#24364b'; BLUE = '#eaf2fb'; LINE = '#64758a'; BORDER = '#b7c6d6'; WHITE = '#ffffff'

class Canvas:
    def __init__(self, w, h, title, subtitle=''):
        self.w,self.h=w,h
        self.im=Image.new('RGB',(w,h),WHITE);self.d=ImageDraw.Draw(self.im)
        self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',f'<rect width="{w}" height="{h}" fill="white"/>']
        self.text(w/2,40,title,32,True)
        if subtitle:self.text(w/2,78,subtitle,20)
    def text(self,x,y,text,size=23,bold=False,anchor='middle',color=INK):
        font=ImageFont.truetype(BOLD if bold else REG,size)
        lines=text.split('\n');step=size*1.35
        for i,line in enumerate(lines):
            yy=y+(i-(len(lines)-1)/2)*step
            self.d.text((x,yy),line,font=font,fill=color,anchor={'middle':'mm','start':'lm','end':'rm'}[anchor])
            self.svg.append(f'<text x="{x}" y="{yy}" dominant-baseline="middle" text-anchor="{anchor}" font-family="Segoe UI,Arial,sans-serif" font-size="{size}" font-weight="{600 if bold else 400}" fill="{color}">{escape(line)}</text>')
    def rect(self,x,y,w,h,text='',size=23,fill=BLUE,bold=False):
        self.d.rectangle((x-w/2,y-h/2,x+w/2,y+h/2),fill=fill,outline=BORDER,width=2)
        self.svg.append(f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" fill="{fill}" stroke="{BORDER}" stroke-width="2"/>')
        if text:self.text(x,y,text,size,bold)
    def diamond(self,x,y,w,h,text,size=23):
        pts=[(x,y-h/2),(x+w/2,y),(x,y+h/2),(x-w/2,y)]
        self.d.polygon(pts,fill='#fff5d9',outline=INK,width=2)
        self.svg.append(f'<polygon points="{" ".join(f"{a},{b}" for a,b in pts)}" fill="#fff5d9" stroke="{INK}" stroke-width="2"/>')
        self.text(x,y,text,size,True)
    def path(self,pts,label=None,at=None):
        self.d.line(pts,fill=LINE,width=3)
        a,b=pts[-2],pts[-1];theta=math.atan2(b[1]-a[1],b[0]-a[0]);size=11
        head=[b,(b[0]-size*math.cos(theta-.45),b[1]-size*math.sin(theta-.45)),(b[0]-size*math.cos(theta+.45),b[1]-size*math.sin(theta+.45))]
        self.d.polygon(head,fill=LINE)
        self.svg.append(f'<polyline points="{" ".join(f"{x},{y}" for x,y in pts)}" fill="none" stroke="{LINE}" stroke-width="3"/>')
        self.svg.append(f'<polygon points="{" ".join(f"{x},{y}" for x,y in head)}" fill="{LINE}"/>')
        if label:self.text(*(at or pts[0]),label,21,True)
    def save(self,name):
        self.im.save(OUT/f'{name}.png');(OUT/f'{name}.svg').write_text('\n'.join(self.svg+['</svg>']),encoding='utf-8')

c=Canvas(1250,1000,'High Level Attendance','D365FO  |  File TXT manual  |  Shift sebagai acuan')
cx=760
nodes=[(155,'IT / Attendance Operator\nMenyiapkan file TXT'),(290,'HR Admin upload\nAttendance Staging'),(425,'HR memilih record\nKlik Process'),(560,'Pemetaan punch terhadap shift\nPembentukan / pembaruan Attendance'),(695,'HR memeriksa dan mengoreksi\nEmployee Attendance'),(830,'Laporan dan Payroll\nMenggunakan nilai attendance tersimpan')]
for y,t in nodes:c.rect(cx,y,580,85,t)
for (y,_),(ny,_) in zip(nodes,nodes[1:]):c.path([(cx,y+43),(cx,ny-43)])
c.rect(230,560,355,110,'Working Schedule\nTanggal dan jam shift efektif',22)
c.path([(407,560),(470,560)])
c.text(625,935,'Staging: raw punch dan Status per record. Attendance: In/Out, durasi Float dan koreksi HR.',21)
c.save('attendance-high-level')

c=Canvas(1500,2600,'System Flow Attendance','Kotak = aktivitas  |  Belah ketupat = decision  |  Cabang Ya / Tidak')
main=1050;side=350
c.rect(main,150,550,80,'HR klik Upload File\nPeriksa format isi TXT')
c.diamond(main,295,320,130,'Format\nsesuai?')
c.path([(main,190),(main,230)])
c.rect(side,295,480,95,'Tampilkan error format\nIT / Operator perbaiki dan export ulang',21)
c.path([(890,295),(590,295)],'Tidak',(725,270))
c.path([(110,295),(55,295),(55,150),(775,150)])
c.rect(main,450,550,80,'Simpan record pada Staging\nStatus Pending')
c.path([(main,360),(main,410)],'Ya',(1090,383))
c.rect(main,580,550,80,'HR memilih record\nKlik Process')
c.path([(main,490),(main,540)])
c.rect(main,715,550,90,'Lapis 1\nValidasi dan konversi seluruh pilihan')
c.path([(main,620),(main,670)])
c.diamond(main,875,350,145,'Seluruh pilihan\nberhasil?')
c.path([(main,760),(main,802)])
c.rect(main,1040,550,80,'Simpan hasil Attendance\nStatus record diperbarui')
c.path([(main,948),(main,1000)],'Ya',(1090,974))
c.rect(side,875,490,90,'Rollback percobaan bersama\nMulai fallback per record',22)
c.path([(875,875),(595,875)],'Tidak',(735,848))
c.rect(side,1040,490,80,'Ambil record berikutnya\nUrut employee dan timestamp',22)
c.path([(side,920),(side,1000)])
c.rect(side,1170,490,80,'Validasi dan konversi\nrecord tersebut',22)
c.path([(side,1080),(side,1130)])
c.diamond(side,1325,280,130,'Record\nberhasil?')
c.path([(side,1210),(side,1260)])
c.rect(170,1475,285,85,'Simpan hasil\nProcessed / Duplicate',21)
c.rect(570,1475,310,85,'Rollback record\nFailed dan pesan error',21)
c.path([(210,1325),(170,1325),(170,1432)],'Ya',(145,1390))
c.path([(490,1325),(570,1325),(570,1432)],'Tidak',(620,1390))
c.diamond(side,1640,310,130,'Masih ada\nrecord?')
c.path([(170,1518),(170,1545),(side,1545),(side,1575)])
c.path([(570,1518),(570,1545),(side,1545)])
c.path([(195,1640),(15,1640),(15,1040),(105,1040)],'Ya',(125,1610))
c.rect(main,1800,550,90,'HR membuka Employee Attendance\nMemeriksa In/Out dan flag')
c.path([(side,1705),(side,1800),(775,1800)],'Tidak',(410,1770))
c.path([(main,1080),(main,1755)])
c.diamond(main,1965,310,130,'Perlu\nkoreksi?')
c.path([(main,1845),(main,1900)])
c.rect(side,1965,490,90,'HR klik Edit\nUbah attendance dan klik Save',22)
c.path([(895,1965),(595,1965)],'Ya',(750,1938))
c.rect(side,2110,490,80,'Perbarui perhitungan\nSimpan audit; raw tetap utuh',22)
c.path([(side,2010),(side,2070)])
c.path([(side,2150),(side,2210),(700,2210),(700,1800),(775,1800)])
c.rect(main,2290,550,95,'HR selesai memverifikasi\nData digunakan pada laporan / payroll',22)
c.path([(main,2030),(main,2242)],'Tidak',(1090,2115))
c.text(750,2460,'Record Failed dapat di-Retry setelah penyebab diperbaiki. Jika sumber salah, upload ulang file perbaikan.',21)
c.text(750,2505,'Tidak ada Status batch. Missing Out adalah flag Attendance, bukan kegagalan otomatis Staging.',21)
c.save('attendance-system-flow')

c=Canvas(1250,1190,'Pemetaan Punch Berdasarkan Shift','Timestamp TXT + working schedule efektif menentukan tanggal kerja dan arah punch')
cx=800
c.rect(cx,165,610,85,'Baca employee dan timestamp punch\nCari shift termasuk hari sebelumnya',23)
c.diamond(cx,330,340,135,'Satu shift\ncocok?')
c.path([(cx,208),(cx,262)])
c.rect(225,330,370,100,'Failed\nShift tidak ada / ambigu',21)
c.path([(630,330),(410,330)],'Tidak',(515,300))
c.rect(cx,495,610,90,'Tanggal kerja = tanggal mulai shift\nKelompokkan ke rentang In / Out')
c.path([(cx,398),(cx,450)],'Ya',(840,424))
c.diamond(cx,665,340,135,'Peran punch\ndapat ditentukan?')
c.path([(cx,540),(cx,597)])
c.rect(225,665,370,100,'Failed\nPunch ambigu',21)
c.path([(630,665),(410,665)],'Tidak',(515,634))
c.rect(cx,855,610,110,'Bentuk / perbarui Attendance shift terkait\nOut berikutnya melengkapi record existing\nKoreksi HR tidak ditimpa otomatis',22)
c.path([(cx,733),(cx,800)],'Ya',(840,767))
c.rect(cx,1040,610,90,'Hitung durasi Float dan late / early leave\nOut kosong: durasi 0.0, Missing Out aktif',22)
c.path([(cx,910),(cx,995)])
c.text(625,1140,'Rentang In/Out, banyak punch, dan konflik shift perlu aturan final sebelum development.',21)
c.save('attendance-shift-pairing')

def mock_base(title,actions,height=1080):
    c=Canvas(1500,height,'')
    c.im=Image.new('RGB',(1500,height),WHITE);c.d=ImageDraw.Draw(c.im)
    c.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="{height}"><rect width="1500" height="{height}" fill="white"/>']
    c.rect(750,35,1500,70,fill='#002050')
    c.text(35,35,'Dynamics 365  |  Finance and Operations',24,True,'start','#ffffff')
    c.text(1440,35,'HOGY  ·  HR Admin',22,False,'end','#ffffff')
    c.text(40,112,title,34,False,'start')
    c.text(1440,112,'Konsep · Data ilustrasi',19,False,'end')
    x=40
    for action in actions:
        w=len(action)*12+34
        c.rect(x+w/2,180,w,46,action,20,fill='#f6f7f9');x+=w+14
    return c

def table(c,top,columns,widths,rows):
    c.rect(750,top+23,1420,46,fill='#f0f3f6')
    xs=[];x=40
    for col,w in zip(columns,widths):xs.append(x);c.text(x+12,top+23,col,19,True,'start');x+=w
    for ri,row in enumerate(rows):
        yy=top+46+ri*62
        c.rect(750,yy+31,1420,62,fill='#edf4fb' if ri==0 else WHITE)
        for x,value in zip(xs,row):c.text(x+12,yy+31,value,19,False,'start')

c=mock_base('Attendance Staging',['Upload File','Process','Retry','View Errors','Open Attendance'],1000)
c.text(40,255,'Legal Entity  [ HOGY ]     Punch Date  [ From ... To ... ]     Status  [ All ]',21,False,'start')
table(c,295,['Select','Source NPK','Punch Timestamp','Employee','Status','Error'],[90,160,280,240,160,490],[
    ['[x]','001198','07/10/2026 22:58','Ari Saputra','Processed','—'],
    ['[x]','999999','08/10/2026 07:00','—','Failed','Employee tidak ditemukan'],
    ['','001198','08/10/2026 07:01','Ari Saputra','Pending','—']])
c.text(40,585,'▼  Selected Record',23,True,'start')
for x,y,label,value in [(40,645,'Legal Entity','HOGY'),(530,645,'Source NPK','001198'),(1000,645,'Status','Processed'),(40,740,'Punch Timestamp','07/10/2026 22:58'),(530,740,'Resolved Employee','Ari Saputra'),(1000,740,'Error Message','—')]:
    c.text(x,y,label,18,False,'start');c.text(x,y+34,value,22,False,'start')
c.text(40,855,'+  Source Data',23,True,'start')
c.text(40,940,'Satu Status per record. Tidak ada BatchId, RowNumber, atau tombol Validate.',20,False,'start')
c.save('mockup-attendance-staging')

c=mock_base('Employee Attendance',['Edit','Save','View Fingerprint','View Schedule','Related Leave','Related Overtime'],1230)
c.text(40,255,'Legal Entity  [ HOGY ]     Work Date  [ From ... To ... ]     Employee  [ All ]     Flag  [ All ]',21,False,'start')
table(c,295,['NPK / Employee','Work Date','Actual In','Actual Out','Hours','Late','Early','Flag'],[260,170,245,245,100,100,100,200],[
    ['001198 · Ari Saputra','07/10/2026','07/10/2026 22:58','08/10/2026 07:01','8.05','0.0','0.0','—'],
    ['001208 · Citra Dewi','08/10/2026','08/10/2026 07:03','—','0.0','1.0','0.0','Missing Out']])
c.text(40,530,'▼  Working Schedule',23,True,'start')
for x,y,label,value in [(40,590,'Work Date','07/10/2026'),(530,590,'Schedule In','07/10/2026 23:00'),(1000,590,'Schedule Out','08/10/2026 07:00')]:
    c.text(x,y,label,18,False,'start');c.text(x,y+34,value,22,False,'start')
c.text(40,700,'▼  Attendance',23,True,'start')
for x,y,label,value in [(40,755,'Actual In','07/10/2026 22:58'),(530,755,'Actual Out','08/10/2026 07:01')]:
    c.text(x,y,label,18,False,'start');c.rect(x+205,y+46,410,48,value,21,fill=WHITE)
c.text(1000,755,'Actual Work Hours',18,False,'start');c.text(1000,791,'8.05',22,False,'start')
c.text(40,860,'Late Minutes  0.0      Early Leave Minutes  0.0      Tolerance  2 minutes',21,False,'start')
c.text(40,935,'+  Flags and Remarks',23,True,'start')
c.text(40,1005,'+  Source History',23,True,'start')
c.text(40,1100,'HR mengoreksi langsung pada Attendance dan memverifikasi sebelum payroll.',21,False,'start')
c.text(40,1145,'Durasi tanpa Out = 0.0. Flag tidak memberikan nilai pengganti kepada payroll.',21,False,'start')
c.save('mockup-employee-attendance')
print('Created 5 PNG and 5 editable SVG assets')
