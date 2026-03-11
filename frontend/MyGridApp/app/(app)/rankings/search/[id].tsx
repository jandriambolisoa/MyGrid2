import { View } from "react-native";
import { Colors } from "@/theme";
import { useLocalSearchParams } from "expo-router";
import { useApi } from "@/hooks";
import { useAuth } from "@/contexts/AuthContext";
import { useEffect, useState } from "react";
import { Header, RankingsFooter, UserPredictionsList } from "@/components/widgets";

export default function Search () {

  const auth = useAuth();
  const local = useLocalSearchParams();
  const event = local.event ? JSON.parse(local.event as any) : null;
  const item = local.item ? JSON.parse(local.item as any): null;

  const { datas, error, loading, api: getPredictions } = useApi(true);

  const [headerHeight, setHeaderHeight] = useState(0);
  const [footerHeight, setFooterHeight] = useState(0);
  const [listDatas, setListDatas] = useState([]);

  useEffect(() => {
    auth && getPredictions({
      endpoint: `/events/sessions/predictions/search?user_id=${item?.user?.id}`,
      auth: auth
    })
  }, [auth])

  useEffect(() => {
    if (datas?.sessions?.length && !listDatas.length) {
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
        spotColor={event?.colors?.[0]}
        title={item?.user?.username}
        subtitle={event?.name}
      />
      <RankingsFooter
        onLayout={(e: any) => setFooterHeight(e.nativeEvent.layout.height)}
        datas={item}
        spotColor={color2}
        self={false}
      />
    </View>
  )
}