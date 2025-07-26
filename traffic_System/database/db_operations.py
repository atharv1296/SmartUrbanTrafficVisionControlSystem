import json
from datetime import datetime
from .db_setup import create_db_connection

def log_traffic_data(direction, data):
    conn = None
    try:
        conn = create_db_connection()
        if not conn:
            print("Couldn't connect to database")
            return

        cursor = conn.cursor(buffered=True)

        if data['speeds']:
            valid_speeds = [s for s in data['speeds'] if not (math.isnan(s) or math.isinf(s))]
            avg_speed = np.mean(valid_speeds) if valid_speeds else None
        else:
            avg_speed = None

        congestion_index = (data['total'] / 50) * (1 - (avg_speed / 60)) if avg_speed else None
        vehicle_types = json.dumps(data['types'])
        positions = json.dumps([{"x1": p[0], "y1": p[1], "x2": p[2], "y2": p[3]} for p in data['positions']])

        query = """
        INSERT INTO traffic_data 
        (timestamp, direction, vehicle_count, ambulance_count, 
         avg_speed, congestion_index, vehicle_types, positions)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            datetime.now(),
            direction,
            int(data['total']),
            int(data['ambulance']),
            float(avg_speed) if avg_speed else None,
            float(congestion_index) if congestion_index else None,
            vehicle_types,
            positions
        ))
        conn.commit()
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()