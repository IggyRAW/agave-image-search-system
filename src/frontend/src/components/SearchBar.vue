<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useSearchStore } from '@/stores/searchStore'

const searchStore = useSearchStore()

const searchWord = ref<string>('')

onMounted(() => {
  onSearch()
})

const onSearch = () => {
  searchStore.setSearchWord(searchWord.value)
  searchStore.setSearchType(0)
  searchStore.fetchSearchList()
}
</script>

<template>
  <v-container>
    <v-text-field
      v-model="searchWord"
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
