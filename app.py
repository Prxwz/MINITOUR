from flask import Flask, render_template
import folium
from folium.plugins import BeautifyIcon

app = Flask(__name__)

@app.route('/')
def index():
    # ข้อมูลสถานที่ 5 จุด (จุดเริ่มต้น กทม. และจุดท่องเที่ยว)
    locations = [
        {
            "id": 1,
            "name": "จุดนัดพบ: กรุงเทพมหานคร",
            "lat": 13.755226783290112,
            "lon": 100.49714054182805,
            "desc": "จุดเริ่มต้นการเดินทางยามเช้า สัมผัสวิถีชีวิตริมแม่น้ำเจ้าพระުރและเมืองหลวงอันทรงคุณค่าทางประวัติศาสตร์",
            "image": "https://static.thairath.co.th/media/dFQROr7oWzulq5Fa4MDnIPhZPsqmRTyDeuiDAt6yLwmE0DanaG3wbxTKtKTMLCKfjEb.jpg",
            "google_maps": "https://www.google.com/maps/search/?api=1&query=13.755226783290112,100.49714054182805"
        },
        {
            "id": 2,
            "name": "พระบรมมหาราชวัง & วัดพระแก้ว",
            "lat": 13.751791909095356,
            "lon": 100.49268592014727,
            "desc": "สถาปัตยกรรมไทยอันวิจิตรงดงามตระการตา ศูนย์รวมจิตใจและศิลปะชั้นครูแห่งกรุงรัตนโกสินทร์",
            "image": "https://cdn.royalgrandpalace.th/images/history/sec1_dt.jpg",
            "google_maps": "https://www.google.com/maps/search/?api=1&query=13.751791909095356,100.49268592014727"
        },
        {
            "id": 3,
            "name": "วัดโพธิ์ (วัดพระเชตุพนฯ)",
            "lat": 13.746771810063171,
            "lon": 100.49335593446985,
            "desc": "นมัสการพระพุทธไสยาสน์องค์ใหญ่ ชมความงามของกระเบื้องเคลือบและแหล่งกำเนิดนวดแผนไทยโบราณ",
            "image": "https://www.watpho.com/public/images/content/content_26308-12-2018%2021_01_10.jpg",
            "google_maps": "https://www.google.com/maps/search/?api=1&query=13.746771810063171,100.49335593446985"
        },
        {
            "id": 4,
            "name": "วัดอรุณราชวราราม (วัดอรุณฯ)",
            "lat": 13.744021684396788,
            "lon": 100.48795859324628,
            "desc": "ยลโฉมพระปรางค์ประดับกระเบื้องเคลือบโบราณริมน้ำ งดงามโดดเด่นยามแสงอาทิตย์สาดส่อง",
            "image": "https://www.novotelbkk.com/wp-content/uploads/sites/62/2016/11/Destination-Temple-of-the-Dawn.jpg",
            "google_maps": "https://www.google.com/maps/search/?api=1&query=13.744021684396788,100.48795859324628"
        },
        {
            "id": 5,
            "name": "ไอคอนสยาม (IconSiam)",
            "lat": 13.726004300829532,
            "lon": 100.51002681173283,
            "desc": "ปิดท้ายวันด้วยการพักผ่อน ช้อปปิ้ง และสัมผัสประสบการณ์ริมแม่น้ำในบรรยากาศร่วมสมัยระดับโลก",
            "image": "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/24/58/07/d4/iconsiam.jpg?w=1200&h=-1&s=1",
            "google_maps": "https://www.google.com/maps/search/?api=1&query=13.726004300829532,100.51002681173283"
        }
    ]

    # สร้างแผนที่กลางด้วย Folium (ศูนย์กลางอยู่ที่พิกัดเฉลี่ย)
    center_lat = 13.7447
    center_lon = 100.4950
    m = folium.Map(location=[center_lat, center_lon], zoom_start=14, tiles='CartoDB Positron')

    # เก็บพิกัดทั้งหมดเพื่อวาดเส้นทาง (Polyline)
    route_coords = []

    for loc in locations:
        route_coords.append([loc["lat"], loc["lon"]])
        
        # ปรับแต่ง Custom Marker ให้เข้ากับแนว Vintage Cinematic (สีทองหรูหรา / ดำคลาสสิก)
        icon = BeautifyIcon(
            icon='bookmark',
            icon_shape='marker',
            background_color='#2C2A29',
            border_color='#D4AF37',
            text_color='#F4F1EA'
        )
        
        popup_html = f"""
        <div style="font-family: 'Playfair Display', serif; width: 200px; color: #2C2A29;">
            <h4 style="margin: 0 0 5px; font-size: 14px; border-bottom: 1px solid #D4AF37; padding-bottom: 3px;">{loc['name']}</h4>
            <p style="font-size: 11px; line-height: 1.4; color: #555;">{loc['desc']}</p>
        </div>
        """
        
        folium.Marker(
            location=[loc["lat"], loc["lon"]],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=loc["name"],
            icon=icon
        ).add_to(m)

    # วาดเส้นทางเชื่อมโยงสถานที่ทั้งหมด
    folium.PolyLine(
        route_coords,
        color="#8C6D46",
        weight=3,
        opacity=0.8,
        dash_array='5, 5'
    ).add_to(m)

    # Render แผนที่เป็น HTML string เพื่อส่งไปแสดงผลใน Template
    map_html = m._repr_html_()

    return render_template('index.html', locations=locations, map_html=map_html)

if __name__ == '__main__':
    app.run(debug=True)