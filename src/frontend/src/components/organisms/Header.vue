<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getNamedList } from '@/api/getNamedList'
import { getProviders, type ProviderModel } from '@/api/getProviders'
import { MYURL, BEATGARDENURL } from '@/environment'
import { useSearchStore } from '@/stores/searchStore'
import { spineTypeList } from '@/api/types/spineType'

const searchStore = useSearchStore()
const drawer = ref(false)
const providers = ref<ProviderModel[]>([])

onMounted(async () => {
  try {
    searchStore.fetchRankingList()
    searchStore.namedList = await getNamedList()
    providers.value = await getProviders()
  } catch (error) {
    console.error(error)
  }
})

// 全検索
async function onAllSearch() {
  searchStore.setSearchWord('')
  searchStore.setSearchType(0)
  searchStore.fetchSearchList()
  closeDrawer()
}

// ネームド検索処理
async function onSearchByNamed(named: string) {
  searchStore.setSearchWord(named)
  searchStore.setSearchType(1)
  searchStore.fetchSearchList()
  closeDrawer()
}

// 提供者検索処理
async function onSearchByProvider(provider: string) {
  searchStore.setSearchWord(provider)
  searchStore.setSearchType(2)
  searchStore.fetchSearchList()
  closeDrawer()
}

// 鋸歯の特徴検索
async function onSearchSpineType(spineType: string) {
  searchStore.setSearchWord(spineType)
  searchStore.setSearchType(4)
  searchStore.fetchSearchList()
  closeDrawer()
}

// ドロワーを閉じる
function closeDrawer() {
  drawer.value = false
  searchStore.scrollToTop()
}
</script>

<template>
  <v-app-bar scroll-threshold="228">
    <v-app-bar-title>
      <img width="250px" height="50px" src="../../assets/title.png" alt="title" loading="lazy" />
      <a :href="MYURL" target="_blank" rel="noopener noreferrer">
        <img width="60px" height="60px" src="../../assets/logo.png" alt="logo" loading="lazy" />
      </a>
    </v-app-bar-title>
    <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
  </v-app-bar>

  <v-navigation-drawer v-model="drawer" location="right" temporary>
    <v-list>
      <v-list-item title="全アガベ検索" value="contact" @click="onAllSearch"></v-list-item>
      <v-list-group>
        <template v-slot:activator="{ props }">
          <v-list-item v-bind="props" title="ネームド一覧"> </v-list-item>
        </template>
        <v-list-item
          v-for="named in searchStore.namedList"
          :key="named.name"
          :title="named.name"
          @click="onSearchByNamed(named.name)"
        ></v-list-item>
      </v-list-group>

      <v-list-group>
        <template v-slot:activator="{ props }">
          <v-list-item v-bind="props" title="提供者一覧"> </v-list-item>
        </template>
        <v-list-item
          v-for="provider in providers"
          :key="provider.username"
          :title="provider.username"
          @click="onSearchByProvider(provider.username)"
        ></v-list-item>
      </v-list-group>

      <v-list-group>
        <template v-slot:activator="{ props }">
          <v-list-item v-bind="props" title="検索ランキング"> </v-list-item>
        </template>
        <v-list-item
          v-for="(ranking, index) in searchStore.rankingList"
          :key="ranking"
          :title="`${index + 1}位 ${ranking}`"
          @click="onSearchByNamed(ranking)"
        ></v-list-item>
      </v-list-group>

      <v-list-group>
        <template v-slot:activator="{ props }">
          <v-list-item v-bind="props" title="鋸歯の特徴で検索"> </v-list-item>
        </template>
        <v-list-item
          v-for="spineType in spineTypeList"
          :key="spineType"
          :title="spineType"
          @click="onSearchSpineType(spineType)"
        ></v-list-item>
      </v-list-group>

      <a :href="MYURL" target="_blank" rel="noopener noreferrer">
        <v-list-item title="お問い合わせ" value="contact"></v-list-item>
      </a>
      <div class="flex-grow-1"></div>
      <a
        :href="BEATGARDENURL"
        target="_blank"
        rel="noopener noreferrer"
        style="text-decoration: none"
      >
        <v-list-item title="BEAT GARDENブログ" value="contact" class="banner-item"></v-list-item>
      </a>
    </v-list>
  </v-navigation-drawer>
</template>

<style scoped>
@font-face {
  font-family: 'MyCustomFont';
  src:
    url('path/to/font.woff2') format('woff2'),
    url('path/to/font.woff') format('woff');
  font-display: swap; /* フォント読み込み中にシステムフォントが表示される */
}

.logo {
  max-width: 100%;
  height: 100%;
}
.banner-item {
  background-image: url('../../assets/beat-garden.png');
  background-size: cover;
  background-position: center;
  height: 70px;
  display: flex;
  align-items: center;
  color: rgb(255, 255, 255);
  justify-content: center;
  font-weight: bold;
  font-size: 18px;
}
</style>
