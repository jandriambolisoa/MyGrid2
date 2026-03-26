import { scopedI18n } from "@/translations/i18n";
import * as SecureStore from "expo-secure-store";

const t = scopedI18n('sessions.predictions')

export async function pasteDatas (datas: any, setDatas: (datas: any) => void, showToast: (datas: any) => void = () => {}) {

  const clipboard = await SecureStore.getItemAsync('clipboard');
  if (clipboard) {
    const ids = JSON.parse(clipboard);
    if (Array.isArray(ids) && ids.length) {
      const pastedDatas = ids.map((number: number) => datas.find((item: any) => item.driver.id === number)).filter((item: any) => item);
      const missingDrivers = datas.filter((item: any) => !ids.find((number: any) => number === item.driver.id));
      pastedDatas.push(...missingDrivers);
      setDatas(pastedDatas);
      return;
    }
  }
  showToast({
    type: 'error',
    title: t('noDatasToPaste'),
    duration: 2500
  })
}