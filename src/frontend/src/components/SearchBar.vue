<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getSearchList, type CardItemModel } from '../api/search'

const emit = defineEmits(['searchList'])

const searchWord = ref<string>('')
const searchList = ref<CardItemModel[]>([])

onMounted(() => {
  onSearch()
})

const onSearch = async () => {
  try {
    console.log(`検索ワード:${searchWord.value}`)
    searchList.value = await getSearchList(searchWord.value)
    emit('searchList', searchList.value)
  } catch (error) {
    console.error('検索エラー：', error)
  }
}
</script>

<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12">
        <v-text-field
          v-model="searchWord"
          append-inner-icon="mdi-magnify"
          density="compact"
          label="キーワードを入力"
          variant="solo"
          hide-details
          single-line
          @click:append-inner="onSearch"
          @keydown.enter="onSearch"
        ></v-text-field>
      </v-col>
    </v-row>
  </v-container>
</template>
