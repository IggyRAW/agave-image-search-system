<script setup lang="ts">
import { onMounted, ref } from 'vue'

import Header from '../components/organisms/Header.vue'
import SearchBar from '@/components/SearchBar.vue'
import CardItem from '@/components/CardItem.vue'
import Pagination from '@/components/Pagination.vue'
import { useSearchStore } from '@/stores/searchStore'

const searchStore = useSearchStore()

const showScrollButton = ref<boolean>(false)

const handleScroll = () => {
  showScrollButton.value = window.scrollY > 300
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)

  // admaxoverlay 設定
  window.admaxoverlay = {
    tag_id: '796a61b6b40635a5f691c10d76fad8f0',
    type: 'o',
  }

  // 広告スクリプトを動的に追加
  const script = document.createElement('script')
  script.src = 'https://adm.shinobi.jp/st/s.js'
  script.type = 'text/javascript'
  script.charset = 'utf-8'
  document.head.appendChild(script)
})
</script>

<template>
  <v-app>
    <Header />
    <v-main>
      <!-- 検索バー -->
      <SearchBar />

      <!-- アイテム -->
      <div
        v-if="searchStore.searchList.length > 0"
        style="max-width: 95%; margin: 0 auto; padding: 16px"
      >
        <div v-if="searchStore.searchType == 0">
          <p>※部分一致検索なので他ネームドも含みます</p>
        </div>
        <v-row>
          <v-col
            v-for="item in searchStore.searchList"
            :key="item.id"
            cols="6"
            xs="6"
            sm="4"
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

      <!-- ページネーション -->
      <Pagination />

      <!-- admax -->
      <div class="ad-container"></div>
      <!-- admax -->

      <!-- トップへ移動ボタン -->
      <v-btn v-if="showScrollButton" class="scroll-to-top" @click="searchStore.scrollToTop()" icon>
        <v-icon>mdi-arrow-up</v-icon>
      </v-btn>
    </v-main>
  </v-app>
</template>

<style scoped>
@font-face {
  font-family: 'MyCustomFont';
  src:
    url('path/to/font.woff2') format('woff2'),
    url('path/to/font.woff') format('woff');
  font-display: swap; /* フォント読み込み中にシステムフォントが表示される */
}

.scroll-to-top {
  position: fixed;
  bottom: 70px;
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

.pagination-container {
  display: flex;
  justify-content: center;
  padding: 16px;
}

#ad-container {
  width: 100%;
  text-align: center;
}
</style>
