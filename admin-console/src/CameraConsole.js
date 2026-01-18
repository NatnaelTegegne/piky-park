import React, { useState, useEffect } from 'react';
import axios from 'axios';

const CameraConsole = () => {
    const [videoUrl, setVideoUrl] = useState(null);
    const [parkingStatus, setParkingStatus] = useState({});
    const [statusMsg, setStatusMsg] = useState("Initializing...");
    
    // 📏 DYNAMIC SCALING STATE
    const [scaleFactor, setScaleFactor] = useState({ x: 1, y: 1 });
    
    // API ENDPOINTS
    const API_CONFIG = 'http://localhost:5000/config';
    const API_DETECT = 'http://localhost:5000/detect_frame';


    //  MASTER CONFIGURATION (CORRECTED 1920x1080 COORDS)

    const SYSTEM_CONFIG = {
        spot_1: { coords: [806, 562, 972, 622], lat: 37.770650, lng: -122.467800, name: 'Spot 1' },
        spot_2: { coords: [520, 1006, 824, 1072], lat: 37.770700, lng: -122.467700, name: 'Spot 2' },
        spot_3: { coords: [1360, 824, 1670, 980], lat: 37.770750, lng: -122.467800, name: 'Spot 3' },
        spot_4: { coords: [1446, 570, 1632, 640], lat: 37.770800, lng: -122.467600, name: 'Spot 4' },
        spot_5: { coords: [1590, 572, 1792, 638], lat: 37.770850, lng: -122.467800, name: 'Spot 5' },
        spot_6: { coords: [1536, 508, 1708, 562], lat: 37.770900, lng: -122.467500, name: 'Spot 6' },
        spot_7: { coords: [1456, 418, 1566, 444], lat: 37.770950, lng: -122.467800, name: 'Spot 7' },
        spot_8: { coords: [1250, 416, 1336, 444], lat: 37.771000, lng: -122.467400, name: 'Spot 8' },
        spot_9: { coords: [824, 412, 928, 436], lat: 37.771050, lng: -122.467800, name: 'Spot 9' },
        spot_10: { coords: [614, 416, 720, 440], lat: 37.771100, lng: -122.467300, name: 'Spot 10' },
        spot_11: { coords: [408, 412, 518, 436], lat: 37.771150, lng: -122.467800, name: 'Spot 11' },
        spot_12: { coords: [864, 380, 952, 392], lat: 37.771200, lng: -122.467200, name: 'Spot 12' },
        spot_13: { coords: [982, 366, 1040, 398], lat: 37.771250, lng: -122.467800, name: 'Spot 13' },
        spot_14: { coords: [1064, 366, 1136, 392], lat: 37.771300, lng: -122.467100, name: 'Spot 14' },
        spot_15: { coords: [1782, 372, 1864, 394], lat: 37.771350, lng: -122.467800, name: 'Spot 15' },
        spot_16: { coords: [1810, 344, 1888, 356], lat: 37.771400, lng: -122.467000, name: 'Spot 16' },
        spot_17: { coords: [1516, 344, 1588, 352], lat: 37.771450, lng: -122.467800, name: 'Spot 17' },
        spot_18: { coords: [1360, 342, 1426, 348], lat: 37.771500, lng: -122.466900, name: 'Spot 18' },
        spot_19: { coords: [1288, 334, 1364, 360], lat: 37.771550, lng: -122.467800, name: 'Spot 19' },
        spot_20: { coords: [1204, 338, 1288, 360], lat: 37.771600, lng: -122.466800, name: 'Spot 20' },
        spot_21: { coords: [1140, 332, 1212, 360], lat: 37.771650, lng: -122.467800, name: 'Spot 21' },
        spot_22: { coords: [1060, 336, 1132, 352], lat: 37.771700, lng: -122.466700, name: 'Spot 22' },
        spot_23: { coords: [984, 334, 1052, 354], lat: 37.771750, lng: -122.467800, name: 'Spot 23' },
        spot_24: { coords: [912, 334, 984, 348], lat: 37.771800, lng: -122.466600, name: 'Spot 24' },
        spot_25: { coords: [840, 332, 910, 346], lat: 37.771850, lng: -122.467800, name: 'Spot 25' },
        spot_26: { coords: [762, 338, 840, 346], lat: 37.771900, lng: -122.466500, name: 'Spot 26' },
        spot_27: { coords: [682, 336, 762, 344], lat: 37.771950, lng: -122.467800, name: 'Spot 27' },
        spot_28: { coords: [604, 332, 684, 352], lat: 37.772000, lng: -122.466400, name: 'Spot 28' },
        spot_29: { coords: [556, 332, 616, 344], lat: 37.772050, lng: -122.467800, name: 'Spot 29' },
        spot_30: { coords: [974, 564, 1124, 634], lat: 37.772100, lng: -122.466300, name: 'Spot 30' },
        spot_31: { coords: [1144, 564, 1296, 634], lat: 37.772150, lng: -122.467800, name: 'Spot 31' },
        spot_32: { coords: [1292, 566, 1476, 640], lat: 37.772200, lng: -122.466200, name: 'Spot 32' },
        spot_33: { coords: [1732, 568, 1916, 640], lat: 37.772250, lng: -122.467800, name: 'Spot 33' },
        spot_34: { coords: [1604, 816, 1912, 980], lat: 37.772300, lng: -122.466100, name: 'Spot 34' },
        spot_35: { coords: [1144, 816, 1392, 988], lat: 37.772350, lng: -122.467800, name: 'Spot 35' },
        spot_36: { coords: [906, 800, 1114, 992], lat: 37.772400, lng: -122.466000, name: 'Spot 36' },
        spot_37: { coords: [600, 822, 876, 962], lat: 37.772450, lng: -122.467800, name: 'Spot 37' },
        spot_38: { coords: [380, 820, 600, 944], lat: 37.772500, lng: -122.465900, name: 'Spot 38' },
        spot_39: { coords: [96, 796, 404, 940], lat: 37.772550, lng: -122.467800, name: 'Spot 39' },
        spot_40: { coords: [12, 780, 194, 884], lat: 37.772600, lng: -122.465800, name: 'Spot 40' },
        spot_41: { coords: [244, 996, 542, 1062], lat: 37.772650, lng: -122.467800, name: 'Spot 41' },
        spot_42: { coords: [856, 1000, 1106, 1072], lat: 37.772700, lng: -122.465700, name: 'Spot 42' },
        spot_43: { coords: [1140, 1006, 1408, 1078], lat: 37.772750, lng: -122.467800, name: 'Spot 43' },
        spot_44: { coords: [20, 980, 232, 1062], lat: 37.772800, lng: -122.465600, name: 'Spot 44' },
        spot_45: { coords: [644, 564, 816, 624], lat: 37.772850, lng: -122.467800, name: 'Spot 45' },
        spot_46: { coords: [484, 556, 652, 618], lat: 37.772900, lng: -122.465500, name: 'Spot 46' },
        spot_47: { coords: [330, 558, 516, 616], lat: 37.772950, lng: -122.467800, name: 'Spot 47' },
        spot_48: { coords: [186, 550, 356, 616], lat: 37.773000, lng: -122.465400, name: 'Spot 48' },
        spot_49: { coords: [54, 548, 210, 610], lat: 37.773050, lng: -122.467800, name: 'Spot 49' },
        spot_50: { coords: [852, 498, 986, 552], lat: 37.773100, lng: -122.465300, name: 'Spot 50' },
        spot_51: { coords: [734, 488, 848, 534], lat: 37.773150, lng: -122.467800, name: 'Spot 51' },
        spot_52: { coords: [1140, 496, 1242, 548], lat: 37.773200, lng: -122.465200, name: 'Spot 52' },
        spot_53: { coords: [1428, 500, 1504, 560], lat: 37.773250, lng: -122.467800, name: 'Spot 53' },
        spot_54: { coords: [1688, 508, 1828, 546], lat: 37.773300, lng: -122.465100, name: 'Spot 54' },
        spot_55: { coords: [1820, 480, 1916, 524], lat: 37.773350, lng: -122.467800, name: 'Spot 55' },
        spot_56: { coords: [1556, 418, 1668, 440], lat: 37.773400, lng: -122.465000, name: 'Spot 56' },
        spot_57: { coords: [1348, 412, 1462, 440], lat: 37.773450, lng: -122.467800, name: 'Spot 57' },
        spot_58: { coords: [1146, 414, 1232, 436], lat: 37.773500, lng: -122.464900, name: 'Spot 58' },
        spot_59: { coords: [1048, 408, 1136, 444], lat: 37.773550, lng: -122.467800, name: 'Spot 59' },
        spot_60: { coords: [932, 406, 1026, 436], lat: 37.773600, lng: -122.464800, name: 'Spot 60' },
        spot_61: { coords: [716, 412, 820, 436], lat: 37.773650, lng: -122.467800, name: 'Spot 61' },
        spot_62: { coords: [514, 406, 624, 432], lat: 37.773700, lng: -122.464700, name: 'Spot 62' },
        spot_63: { coords: [326, 408, 424, 434], lat: 37.773750, lng: -122.467800, name: 'Spot 63' },
        spot_64: { coords: [428, 360, 528, 384], lat: 37.773800, lng: -122.464600, name: 'Spot 64' },
        spot_65: { coords: [794, 370, 864, 386], lat: 37.773850, lng: -122.467800, name: 'Spot 65' },
        spot_66: { coords: [1442, 358, 1484, 388], lat: 37.773900, lng: -122.464500, name: 'Spot 66' },
        spot_67: { coords: [1680, 376, 1778, 392], lat: 37.773950, lng: -122.467800, name: 'Spot 67' }
    };


    //  INITIALIZATION & CONFIG

    useEffect(() => {
        const sendConfig = async () => {
            try {
                const backendPayload = {};
                Object.keys(SYSTEM_CONFIG).forEach(key => {
                    backendPayload[key] = {
                        lat: SYSTEM_CONFIG[key].lat,
                        lng: SYSTEM_CONFIG[key].lng,
                        name: SYSTEM_CONFIG[key].name,
                        coords: SYSTEM_CONFIG[key].coords 
                    };
                });
                
                await axios.post(API_CONFIG, backendPayload);
                setStatusMsg("✅ GPS & AI Config Sent");
            } catch (err) {
                console.error("Config Error", err);
                setStatusMsg("❌ Backend Offline");
            }
        };
        sendConfig();
    }, []);


    //  REAL-TIME AI LOOP

    useEffect(() => {
        let intervalId = null;

        if (videoUrl) {
            setStatusMsg("🟢 AI Running: Analyzing Video...");
            intervalId = setInterval(() => {
                captureAndSendFrame();
            }, 5000); 
        }

        return () => {
            if (intervalId) clearInterval(intervalId);
        };
    }, [videoUrl]);

 
    //  AUTO-CALCULATE SCALE

    // This fires once the video file is loaded and we know its real size
    const handleMetadata = (e) => {
        const video = e.target;
        const naturalW = video.videoWidth;
        const naturalH = video.videoHeight;
        const displayW = video.offsetWidth; // This is always 900 because we set width="900"
        const displayH = video.offsetHeight;

        console.log(`Video Loaded: Real=${naturalW}x${naturalH} | Display=${displayW}x${displayH}`);

        if (naturalW > 0 && naturalH > 0) {
            // Calculate exact ratio: "How much did we shrink it?"
            const sX = displayW / naturalW;
            const sY = displayH / naturalH;
            setScaleFactor({ x: sX, y: sY });
        }
    };

    const captureAndSendFrame = () => {
        const video = document.getElementById('main-video');
        if (!video) return;

        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        canvas.toBlob(async (blob) => {
            if (!blob) return;
            const formData = new FormData();
            formData.append('frame', blob, 'current_frame.jpg');

            try {
                const response = await axios.post(API_DETECT, formData, {
                    headers: { 'Content-Type': 'multipart/form-data' }
                });
                setParkingStatus(response.data); 
            } catch (err) {
                console.error("Prediction Error:", err);
            }
        }, 'image/jpeg', 0.8);
    };

    const handleFileChange = (e) => {
        if(e.target.files[0]) setVideoUrl(URL.createObjectURL(e.target.files[0]));
    };

    return (
        <div style={{ padding: '20px', background: '#111', minHeight: '100vh', color: 'white', fontFamily: 'sans-serif' }}>
            <div style={{display:'flex', justifyContent:'space-between', alignItems:'center'}}>
                <h1>🅿️ Admin AI Console</h1>
                <h3 style={{color: statusMsg.includes('Offline') || statusMsg.includes('Error') ? 'red' : '#00ff00'}}>
                    {statusMsg}
                </h3>
            </div>

            {!videoUrl && (
                <div style={{border:'2px dashed #444', padding:'40px', textAlign:'center', borderRadius:'10px'}}>
                    <p>Select CCTV Feed to Start AI</p>
                    <input type="file" accept="video/*" onChange={handleFileChange} style={{color:'white'}} />
                </div>
            )}

            {videoUrl && (
                <div style={{ position: 'relative', width: '900px', margin: '20px auto', border: '4px solid #333' }}>
                    
                    {/* VIDEO PLAYER with onLoadedMetadata */}
                    <video 
                        id="main-video"
                        src={videoUrl} 
                        width="900" 
                        onLoadedMetadata={handleMetadata} // Auto-aligns boxes
                        autoPlay loop muted playsInline
                        style={{ display: 'block', width: '100%' }} 
                    />

                    {/* OVERLAY BOXES */}
                    {Object.entries(SYSTEM_CONFIG).map(([spotId, data]) => {
                        const [x1, y1, x2, y2] = data.coords;
                        
                        // Use the Dynamic Scale Factor
                        const w = (x2 - x1) * scaleFactor.x;
                        const h = (y2 - y1) * scaleFactor.y;
                        const left = x1 * scaleFactor.x;
                        const top = y1 * scaleFactor.y;

                        const isOccupied = parkingStatus[spotId] === 'occupied';

                        return (
                            <div key={spotId} style={{
                                position: 'absolute',
                                left: left, top: top, width: w, height: h,
                                border: `2px solid ${isOccupied ? '#ff4444' : '#00cc00'}`,
                                backgroundColor: isOccupied ? 'rgba(255, 0, 0, 0.3)' : 'rgba(0, 255, 0, 0.1)',
                                fontSize: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center',
                                color: 'white', textShadow: '0 0 2px black'
                            }}>
                                {spotId.replace('spot_', '')}
                            </div>
                        );
                    })}
                </div>
            )}
        </div>
    );
};

export default CameraConsole;