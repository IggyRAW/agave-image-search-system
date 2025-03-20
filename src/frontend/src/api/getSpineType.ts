import axios, { AxiosError, type AxiosResponse } from 'axios'
import { type CardItemModel, transformCardItem } from './search'

export const getSpineType = async (
  spine_type: string,
  page: number = 1,
  limit: number = 18,
): Promise<{ total: number; search_list: CardItemModel[] }> => {
  return axios
    .get(`/api/get/spine_type?spine_type=${spine_type}&page=${page}&limit=${limit}`)
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
