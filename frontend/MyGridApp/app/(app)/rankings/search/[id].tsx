import { View } from "react-native";
import { Colors } from "@/theme";
import { useLocalSearchParams, useFocusEffect } from "expo-router";
import { useApi } from "@/hooks";
import { useAuth } from "@/contexts/AuthContext";
import { useEffect, useState, useCallback } from "react";
import { Header, RankingsFooter, UserPredictionsList } from "@/components/widgets";
import { scopedI18n } from "@/translations/i18n";

export default function Search () {

  const auth = useAuth();
  const local = useLocalSearchParams();
  const event = local.event ? JSON.parse(local.event as any) : null;
  const item = local.item ? JSON.parse(local.item as any): null;
  const t = scopedI18n('rankings')

  const { datas, api: getPredictions } = useApi(true);

  const [headerHeight, setHeaderHeight] = useState(0);
  const [footerHeight, setFooterHeight] = useState(0);
  const [listDatas, setListDatas] = useState([]);

  useFocusEffect(
    useCallback(() => {
      if (auth) {
        getPredictions({
          endpoint: `/events/sessions/predictions/search?user_id=${item?.user?.id}`,
          auth: auth
        })
      }
    }, [auth])
  );

  useEffect(() => {
    if (datas?.sessions?.length) {
      if (!event) {
        const newDatas = datas.sessions.filter(
          (item: any) => item.score !== null
        );

        setListDatas(newDatas);
        return;
      }

      const newDatas = datas.sessions.filter(
        (item: any) => item.event_id === event.id && item.score !== null
      );

      setListDatas(newDatas);
    }
  }, [datas])

  const color1 = event?.colors[0];
  const color2 = event?.colors.length > 1 ? event?.colors[1] : color1;

  return (
    <View style={{ flex: 1, backgroundColor: Colors.light.background }}>
      {listDatas.length && <UserPredictionsList
        datas={listDatas}
        footerHeight={footerHeight}
        headerHeight={headerHeight}
        userId={Number(local.id)}
      />}
      <Header 
        onLayout={(e: any) => setHeaderHeight(e.nativeEvent.layout.height)}
        spotColor={event? color1 : local.userColor}
        title={item?.user?.username}
        subtitle={event? event.name : t('globalRankings')}
      />
      <RankingsFooter
        onLayout={(e: any) => setFooterHeight(e.nativeEvent.layout.height)}
        datas={item}
        spotColor={event? color2 : local.userColor}
        self={false}
      />
    </View>
  )
}