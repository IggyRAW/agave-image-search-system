import axios, { AxiosError, type AxiosResponse } from 'axios'
import { type CardItemModel, transformCardItem } from './search'

export interface ProviderModel {
  username: string
}

export const getProviders = async (): Promise<ProviderModel[]> => {
  return axios
    .get(`/api/get/providers`)
    .then((res: AxiosResponse<ProviderModel[]>) => {
      return sortList(res.data)
    })
    .catch((err: AxiosError) => {
      console.error(err.message)
      throw err
    })
}

const sortList = (list: ProviderModel[]) => {
  return [...list].sort((a, b) => a.username.localeCompare(b.username, 'ja'))
}

export const getSearchListByProvider = async (
  provider: string,
  page: number = 1,
  limit: number = 18,
): Promise<{ total: number; search_list: CardItemModel[] }> => {
  return axios
    .get(`/api/search_provider?provider=${provider}&page=${page}&limit=${limit}`)
    .then((res: AxiosResponse<{ total: number; search_list: CardItemModel[] }>) => {
      return {
        total: res.data.total,
        search_list: sortListByName(res.data.search_list.map(transformCardItem)),
      }
    })
    .catch((err: AxiosError) => {
      console.error(err.message)
      throw err
    })
}

const sortListByName = (list: CardItemModel[]): CardItemModel[] => {
  return [...list].sort((a, b) => a.name.localeCompare(b.name, 'ja'))
}
