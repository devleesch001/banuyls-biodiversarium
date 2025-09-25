// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Vuetify
import { createVuetify } from 'vuetify'

const myCustomLightTheme = {
  dark: false,
  colors: {
    background: '#eeeeee',
    surface: '#ffffff',
    primary: '#639ca9',
    'primary-darken-1': '#466369',
    secondary: '#76af9d',
    'secondary-darken-1': '#3B574E',
    error: '#ff5947',
    info: '#63a5e2',
    success: '#60c56d',
    warning: '#dad36b',
  }
}

export default createVuetify(
  {
    theme:{      
      defaultTheme: 'myCustomLightTheme',
      themes: {
        myCustomLightTheme,
      }
    }
  }
  // https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
)
