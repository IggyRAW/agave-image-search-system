<script setup lang="ts">
import { ref } from 'vue'
import { type UploadAgaveModel } from '@/api/types/uploadAgave'
import { postAgaveObj } from '@/api/postAgaveObj'

const name = ref<string>('')
const username = ref<string>('')
const filename = ref<string>('')
const usernameSource = ref<string>('')
const source = ref<string>('')
const originCountry = ref<string>('')
const file = ref<File | null>()
const isDisplay = ref<boolean>(true)
const sourceName = ref<string>('')
const imageSource = ref<string>('')

const onFileChange = (newFile: File | File[] | null) => {
  if (!newFile) {
    file.value = null
    filename.value = ''
    return
  }

  // 配列かどうかをチェックし、単一ファイルのみ受け付ける
  if (Array.isArray(newFile)) {
    console.warn('複数ファイルは選択できません')
    return
  }

  file.value = newFile
  filename.value = newFile.name
}

const onSave = async () => {
  if (!file.value) {
    console.error('ファイルが選択されていません。')
    return
  }

  const uploadAgaveObj: UploadAgaveModel = {
    name: name.value,
    username: username.value,
    username_source: usernameSource.value,
    image_file: file.value,
    image_file_path: filename.value,
    source: source.value,
    sourcename: sourceName.value,
    image_source: imageSource.value,
    origin_country: originCountry.value,
    is_display: isDisplay.value,
  }
  console.log(uploadAgaveObj)

  const isSuccess = await postAgaveObj(uploadAgaveObj)
  if (isSuccess) {
    console.log('データを格納しました。')
  } else {
    console.error('データの格納に失敗しました。')
  }
}
</script>

<template>
  <v-app>
    <v-app-bar scroll-threshold="228">
      <v-app-bar-title> アガベ管理画面 </v-app-bar-title>
    </v-app-bar>
    <v-main>
      <v-container>
        <h2>基本情報</h2>
        <v-row>
          <v-col cols="12" md="6"> </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="name"
              clearable
              label="ネームド名"
              variant="solo-filled"
            ></v-text-field>
            <v-file-input
              accept="image/*"
              clearable
              label="画面を選択"
              variant="outlined"
              show-size
              @update:model-value="onFileChange"
            ></v-file-input>
            <v-text-field
              v-model="username"
              clearable
              label="提供者名"
              variant="solo-filled"
            ></v-text-field>
            <v-text-field
              v-model="usernameSource"
              clearable
              label="インスタグラムユーザー名"
              variant="solo-filled"
            ></v-text-field>
            <v-text-field
              v-model="imageSource"
              clearable
              label="インスタグラムポストURL"
              variant="solo-filled"
            ></v-text-field>
            <v-text-field
              v-model="source"
              clearable
              label="購入元"
              variant="solo-filled"
            ></v-text-field>
            <v-text-field
              v-model="sourceName"
              clearable
              label="購入元インスタグラムユーザー名"
              variant="solo-filled"
            ></v-text-field>
            <v-text-field
              v-model="originCountry"
              clearable
              label="原産国"
              variant="solo-filled"
            ></v-text-field>
          </v-col>
          <v-checkbox v-model="isDisplay" label="表示/非表示"></v-checkbox>
          <v-col cols="12" md="6">
            <v-btn color="primary" @click="onSave">保存</v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>
