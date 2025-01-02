<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getProviders, getSearchList, type CardItemModel } from '../../api/getProviders'
import { MYURL } from '@/environment'
const drawer = ref(false)
const emit = defineEmits(['searchList'])
const searchList = ref<CardItemModel[]>([])
const providers = ref()

onMounted(async () => {
  try {
    providers.value = await getProviders()
  } catch (error) {
    console.error(error)
  }
})

async function onSearchProvide(provider: string) {
  searchList.value = await getSearchList(provider)
  emit('searchList', searchList.value)
  drawer.value = false
}
</script>

<template>
  <v-app-bar scroll-behavior="hide fade-image" scroll-threshold="228">
    <v-app-bar-title>
      <img width="250px" height="50px" src="../../assets/title.png" alt="title" />
      <a :href="MYURL" target="_blank" rel="noopener noreferrer">
        <img width="60px" height="60px" src="../../assets/logo.png" alt="logo" />
      </a>
    </v-app-bar-title>
    <v-spacer></v-spacer>
    <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
  </v-app-bar>

  <v-navigation-drawer v-model="drawer" location="right" temporary>
    <v-list>
      <v-list-group>
        <template v-slot:activator="{ props }">
          <v-list-item v-bind="props" title="提供者一覧"> </v-list-item>
        </template>
        <v-list-item
          v-for="provider in providers"
          :key="provider"
          :title="provider"
          @click="onSearchProvide(provider)"
        ></v-list-item>
      </v-list-group>
      <a :href="MYURL" target="_blank" rel="noopener noreferrer">
        <v-list-item title="お問い合わせ" value="contact"></v-list-item>
      </a>
    </v-list>
  </v-navigation-drawer>
</template>

<style scoped>
.logo {
  max-width: 100%;
  height: 100%;
}
</style>
