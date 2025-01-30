import { getSearchList, type CardItemModel } from '@/api/search'
import { getSearchListByNamed } from '@/api/getNamedList'
import { defineStore } from 'pinia'
import { getSearchListByProvider } from '@/api/getProviders'

export const useSearchStore = defineStore('search', {
  state: () => ({
    searchWord: '',
    searchType: 0, // 0:標準検索 1:ネームド検索 2:提供者検索
    currentPage: 1,
    totalPage: 0,
    limit: 18,
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

    setTotalPage(totalPage: number) {
      this.totalPage = totalPage
    },

    async fetchSearchList() {
      try {
        console.log(`検索ワード: ${this.searchWord}, ページ: ${this.currentPage}`)

        let data
        if (this.searchType === 0) {
          data = await getSearchList(this.searchWord, this.currentPage, this.limit)
        } else if (this.searchType === 1) {
          data = await getSearchListByNamed(this.searchWord, this.currentPage, this.limit)
        } else {
          data = await getSearchListByProvider(this.searchWord, this.currentPage, this.limit)
        }

        // トータルページ数の計算
        this.totalPage = Math.ceil(data.total / this.limit)

        this.searchList = data.search_list
      } catch (error) {
        console.error('検索エラー：', error)
      }
    },

    nextPage() {
      this.fetchSearchList()
    },
  },
})
