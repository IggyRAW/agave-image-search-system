<script setup lang="ts">
import { onMounted } from 'vue'
import { useSearchStore } from '@/stores/searchStore'

const searchStore = useSearchStore()

onMounted(() => {
  onSearch()
})

const onSearch = () => {
  searchStore.setSearchWord(searchStore.searchWord)
  searchStore.setSearchType(0)
  searchStore.fetchSearchList()

  // 検索実行時にキーボードを閉じる
  const el = document.activeElement as HTMLElement | null
  if (el) {
    el.blur()
  }
}
</script>

<template>
  <v-container>
    <v-text-field
      v-model="searchStore.searchWord"
      append-inner-icon="mdi-magnify"
      density="compact"
      placeholder="キーワードを入力"
      variant="solo"
      hide-details
      single-line
      @click:append-inner="onSearch"
      @keypress.enter="onSearch"
    >
    </v-text-field>
  </v-container>
</template>
