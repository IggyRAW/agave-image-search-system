import axios, { AxiosError, type AxiosResponse } from 'axios'
import { type UploadAgaveModel } from './types/uploadAgave'

export const postAgaveObj = async (obj: UploadAgaveModel) => {
  const formData = new FormData()
  formData.append('name', obj.name)
  formData.append('username', obj.username)
  formData.append('username_source', obj.username_source)
  formData.append('image_file', obj.image_file)
  formData.append('image_file_path', obj.image_file_path)
  formData.append('source', obj.source)
  formData.append('sourcename', obj.sourcename)
  formData.append('image_source', obj.image_source)
  if (obj.origin_country) formData.append('origin_country', obj.origin_country)
  formData.append('is_display', obj.is_display.toString())

  return await axios
    .post(`/api/post/data`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    .then((res: AxiosResponse<boolean>) => res.data)
    .catch((err: AxiosError) => {
      console.error(err.message)
      throw err
    })
}
