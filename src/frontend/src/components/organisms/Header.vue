<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getSearchList } from '@/api/search'
import { getNamedList, type NamedModel } from '@/api/getNamedList'
import {
  getProviders,
  getSearchListByProvider,
  type CardItemModel,
  type ProviderModel,
} from '@/api/getProviders'
import { MYURL } from '@/environment'

const drawer = ref(false)
const emit = defineEmits(['searchList'])
const searchList = ref<CardItemModel[]>([])
const namedList = ref<NamedModel[]>([])
const providers = ref<ProviderModel[]>([])

onMounted(async () => {
  try {
    namedList.value = await getNamedList()
    providers.value = await getProviders()
  } catch (error) {
    console.error(error)
  }
})

async function onSearch(named: string) {
  searchList.value = await getSearchList(named)
  emit('searchList', searchList.value)
  drawer.value = false
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

async function onSearchProvide(provider: string) {
  searchList.value = await getSearchListByProvider(provider)
  emit('searchList', searchList.value)
  drawer.value = false
  window.scrollTo({ top: 0, behavior: 'smooth' })
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
          <v-list-item v-bind="props" title="ネームド一覧"> </v-list-item>
        </template>
        <v-list-item
          v-for="named in namedList"
          :key="named"
          :title="named"
          @click="onSearch(named)"
        ></v-list-item>
      </v-list-group>
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
