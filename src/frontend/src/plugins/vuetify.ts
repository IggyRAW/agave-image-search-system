import { createVuetify } from 'vuetify'
import {
  VApp,
  VAppBar,
  VAppBarTitle,
  VAppBarNavIcon,
  VMain,
  VBtn,
  VCard,
  VCardTitle,
  VCardSubtitle,
  VCardActions,
  VDialog,
  VCardText,
  VContainer,
  VTextField,
  VIcon,
  VRow,
  VCol,
  VImg,
  VExpandTransition,
  VDivider,
  VList,
  VListGroup,
  VListItem,
  VListItemTitle,
  VNavigationDrawer,
  VTab,
} from 'vuetify/components'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import { VTabs } from 'vuetify/components/VTabs'

const vuetify = createVuetify({
  components: {
    VApp,
    VAppBar,
    VAppBarTitle,
    VAppBarNavIcon,
    VMain,
    VBtn,
    VCard,
    VCardTitle,
    VCardSubtitle,
    VCardActions,
    VDialog,
    VCardText,
    VContainer,
    VTextField,
    VIcon,
    VRow,
    VCol,
    VImg,
    VExpandTransition,
    VDivider,
    VNavigationDrawer,
    VList,
    VListGroup,
    VListItem,
    VListItemTitle,
    VTabs,
    VTab,
  },
  icons: {
    defaultSet: 'mdi',
  },
})

export default vuetify
