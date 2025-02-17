<script setup lang="ts">
import { ref, onMounted, computed, watch, onBeforeUnmount } from 'vue'
import { useSearchStore } from '@/stores/searchStore'
import type { NamedModel } from '@/api/getNamedList'

const showMenu = ref(false)
const searchStore = useSearchStore()
const suggestions = ref<NamedModel[]>([])

onMounted(() => {
  onSearch()
  suggestions.value = searchStore.namedList
  window.addEventListener('scroll', handleScroll)
})

// コンポーネントがアンマウントされる前にリスナーを削除
onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
})

// ネームドリストを監視して更新
watch(
  () => searchStore.namedList,
  (newList) => {
    suggestions.value = newList
  },
)

// 検索ワードからメニューリストを更新
const filteredSuggestions = computed(() => {
  // カタカナに変換
  const convertToKatakana = (str: string) =>
    str.replace(/[\u3041-\u3096]/g, (match: string) =>
      String.fromCharCode(match.charCodeAt(0) + 0x60),
    )

  return searchStore.searchWord
    ? suggestions.value.filter((item) => {
        const searchWordKatakana = convertToKatakana(searchStore.searchWord)
        return item.name.includes(searchWordKatakana)
      })
    : []
})

// メニューリスト選択時処理
const selectSuggestion = (suggestion: string) => {
  searchStore.searchWord = suggestion
  onSearch()
  showMenu.value = false
}

// メニューリストを閉じる
const hideMenu = () => {
  setTimeout(() => (showMenu.value = false), 200)
}

// スクロールイベントでメニューを閉じる
const handleScroll = () => {
  if (showMenu.value) {
    showMenu.value = false
  }
}

// 検索処理
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
      @focus="showMenu = true"
      @blur="hideMenu"
    >
    </v-text-field>
    <v-menu v-model="showMenu" activator="parent" offset-y open-on-hover>
      <v-list v-if="filteredSuggestions.length" dense style="max-height: 200px; overflow-y: auto">
        <v-list-item
          v-for="suggestion in filteredSuggestions"
          :key="suggestion.name"
          @click="selectSuggestion(suggestion.name)"
        >
          <v-list-item-title>{{ suggestion.name }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-container>
</template>
