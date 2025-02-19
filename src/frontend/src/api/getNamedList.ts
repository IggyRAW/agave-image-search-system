import axios, { AxiosError, type AxiosResponse } from 'axios'
import { type CardItemModel, transformCardItem } from './search'

export interface NamedModel {
  name: string
}

export const getNamedList = async (): Promise<NamedModel[]> => {
  return axios
    .get(`/api/get/named/list`)
    .then((res: AxiosResponse<NamedModel[]>) => {
      return sortList(res.data)
    })
    .catch((err: AxiosError) => {
      console.error(err.message)
      throw err
    })
}

const sortList = (list: NamedModel[]) => {
  return [...list].sort((a, b) => a.name.localeCompare(b.name, 'ja'))
}

export const getSearchListByNamed = async (
  search_word: string,
  page: number = 1,
  limit: number = 18,
): Promise<{ total: number; search_list: CardItemModel[] }> => {
  return axios
    .get(`/api/get/named/search?search_word=${search_word}&page=${page}&limit=${limit}`)
    .then((res: AxiosResponse<{ total: number; search_list: CardItemModel[] }>) => {
      return {
        total: res.data.total,
        search_list: res.data.search_list.map(transformCardItem),
      }
    })
    .catch((err: AxiosError) => {
      console.error(err.message)
      throw err
    })
}
