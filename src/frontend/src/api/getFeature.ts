import axios, { AxiosError, type AxiosResponse } from 'axios'

export const getFeature = async (search_word: string): Promise<string> => {
  return axios
    .get(`/api/get/feature?search_word=${search_word}`)
    .then((res: AxiosResponse<string>) => {
      if (res.data == '') {
        return (res.data = '特徴が未登録です')
      }
      return res.data
    })
    .catch((err: AxiosError) => {
      console.error(err.message)
      throw err
    })
}
