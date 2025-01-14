<script setup lang="ts">
import { onMounted, ref } from 'vue'

import Header from '../components/organisms/Header.vue'
import SearchBar from '@/components/SearchBar.vue'
import CardItem from '@/components/CardItem.vue'
import type { CardItemModel } from '../api/search'

// データ受け取り
const receivedSearchList = ref<CardItemModel[]>([])

const showScrollButton = ref<boolean>(false)

const handleSearchList = (list: CardItemModel[]) => {
  receivedSearchList.value = list
}

const handleScroll = () => {
  showScrollButton.value = window.scrollY > 300
}

// ページトップへスクロール
const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})
</script>

<template>
  <v-app>
    <Header @searchList="handleSearchList" />
    <v-main>
      <!-- 検索バー -->
      <SearchBar @searchList="handleSearchList" />

      <!-- アイテム -->
      <div
        v-if="receivedSearchList.length > 0"
        style="max-width: 95%; margin: 0 auto; padding: 16px"
      >
        <v-row>
          <v-col
            v-for="item in receivedSearchList"
            :key="item.id"
            cols="6"
            xs="6"
            sm="6"
            md="3"
            lg="2"
            xl="2"
          >
            <CardItem :item="item" />
          </v-col>
        </v-row>
      </div>
      <div v-else class="no-results">
        <p>該当するアガベがありませんでした</p>
        <p>キーワードを変更して再検索してください</p>
      </div>
      <!-- トップへ移動ボタン -->
      <v-btn v-if="showScrollButton" class="scroll-to-top" @click="scrollToTop" icon>
        <v-icon>mdi-arrow-up</v-icon>
      </v-btn>
    </v-main>
  </v-app>
</template>

<style scoped>
.scroll-to-top {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #28702c;
  color: white;
  border-radius: 50%;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
  z-index: 1000;
}
.no-results {
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 100px;
  margin: 3px auto;
  text-align: center;
}
.no-results p {
  margin: 3px 0;
}
</style>
