const API_URL: string = process.env.REACT_APP_API_URL ?? ""

export const config = {
    CAMERA_OUT: 'http://localhost:8000/out',
    CAMERA_IN: 'http://localhost:8000/in',
    IA_API_TABLET_ANALYZE: `${API_URL}/api/tablet/analyze`
}
