<script setup lang="ts">
import { useSearchStore } from '@/stores/searchStore'
import { computed } from 'vue'
import { useDisplay } from 'vuetify'

const searchStore = useSearchStore()
const { xs, sm, md } = useDisplay()

const paginationVisible = computed(() => {
  if (xs.value) return 3
  if (sm.value) return 5
  if (md.value) return 7
  return 10
})

const loadMore = () => {
  searchStore.nextPage()
  searchStore.scrollToTop()
}
</script>

<template>
  <!-- ページネーション -->
  <div class="pagination-container">
    <v-pagination
      v-model="searchStore.currentPage"
      class="my-1"
      :length="searchStore.totalPage"
      :total-visible="paginationVisible"
      style="color: darkgreen"
      @click="loadMore"
    ></v-pagination>
  </div>
</template>

<style scoped>
@font-face {
  font-family: 'MyCustomFont';
  src:
    url('path/to/font.woff2') format('woff2'),
    url('path/to/font.woff') format('woff');
  font-display: swap; /* フォント読み込み中にシステムフォントが表示される */
}

.pagination-container {
  display: flex;
  justify-content: center;
  padding: 16px;
}
</style>
