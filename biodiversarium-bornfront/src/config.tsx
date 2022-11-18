const API_URL: string = process.env.REACT_APP_API_URL ?? "http://10.3.1.37"

export const config = {
    CAMERA_OUT: 'http://localhost:8000/out',
    CAMERA_IN: 'http://localhost:8000/in',
    IA_API_TABLET_ANALYZE: `${API_URL}/api/tablet/analyze`
}
