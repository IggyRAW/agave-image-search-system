import { getSearchList, type CardItemModel } from '@/api/search'
import { getSearchListByNamed } from '@/api/getNamedList'
import { defineStore } from 'pinia'
import { getSearchListByProvider } from '@/api/getProviders'

export const useSearchStore = defineStore('search', {
  state: () => ({
    searchWord: '',
    searchType: 0, // 0:標準検索 1:ネームド検索 2:提供者検索
    currentPage: 1,
    limit: 20,
    searchList: [] as CardItemModel[],
  }),

  actions: {
    setSearchWord(word: string) {
      this.searchWord = word
      this.currentPage = 1
    },

    setSearchType(type: number) {
      this.searchType = type
    },

    async fetchSearchList() {
      try {
        console.log(`検索ワード: ${this.searchWord}, ページ: ${this.currentPage}`)

        const data = await getSearchList(this.searchWord, this.currentPage, this.limit)

        if (this.currentPage === 1) {
          this.searchList = data
        } else {
          const newItem = data.filter(
            (newItem) => !this.searchList.some((existingItem) => existingItem.id === newItem.id),
          )
          this.searchList.push(...newItem)
        }
      } catch (error) {
        console.error('検索エラー：', error)
      }
    },

    async fetchSearchListByNamed() {
      try {
        console.log(`検索ワード: ${this.searchWord}, ページ: ${this.currentPage}`)

        const data = await getSearchListByNamed(this.searchWord, this.currentPage, this.limit)

        if (this.currentPage === 1) {
          this.searchList = data
        } else {
          const newItem = data.filter(
            (newItem) => !this.searchList.some((existingItem) => existingItem.id === newItem.id),
          )
          this.searchList.push(...newItem)
        }
      } catch (error) {
        console.error('検索エラー：', error)
      }
    },

    async fetchSearchListByProvider() {
      try {
        console.log(`検索ワード: ${this.searchWord}, ページ: ${this.currentPage}`)

        const data = await getSearchListByProvider(this.searchWord, this.currentPage, this.limit)

        if (this.currentPage === 1) {
          this.searchList = data
        } else {
          const newItem = data.filter(
            (newItem) => !this.searchList.some((existingItem) => existingItem.id === newItem.id),
          )
          this.searchList.push(...newItem)
        }
      } catch (error) {
        console.error('検索エラー：', error)
      }
    },

    nextPage() {
      this.currentPage += 1
      if (this.searchType === 0) {
        this.fetchSearchList()
      } else if (this.searchType === 1) {
        this.fetchSearchListByNamed()
      } else {
        this.fetchSearchListByProvider()
      }
    },
  },
})
