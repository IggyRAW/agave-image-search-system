import axios, { AxiosError, type AxiosResponse } from 'axios'

// rankingリストの作成
export const initialized = async (): Promise<[]> => {
  return axios
    .get(`/api/init`)
    .then((res: AxiosResponse<[]>) => {
      return res.data.ranking_list
    })
    .catch((err: AxiosError) => {
      console.error(err.message)
      throw err
    })
}
