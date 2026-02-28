import { useLocalSearchParams } from "expo-router"
import { useAuth } from "@/contexts/AuthContext";
import { useEffect, useState } from "react";
import { View } from "react-native";
import { useApi } from "@/hooks";
import { Header, ScrollContainer, PredictionsList } from "@/components/widgets";
import { niceDatetime } from "@/utils";

export default function Predictions () {

  const auth = useAuth();

  const { id, hasProno } = useLocalSearchParams();
  const { datas, error, loading, api: getPredictions } = useApi()

  console.log(hasProno)

  const [headerHeight, setHeaderHeight] = useState(0);
  const [footerHeight, setFooterHeight] = useState(0);

  useEffect(() => {
    auth && getPredictions({
      endpoint: hasProno === 'true' ? `/events/sessions/predictions/${id}` : `/events/sessions/${id}/drivers`,
      method: 'GET',
      auth: auth
    })
  }, [auth])

  const color1 = datas?.session.event_colors[0]
  const color2 = datas?.session.event_colors.length > 0 ? datas?.session.event_colors[1] : color1

  return (
    <View style={{ flex: 1 }}>
      {datas && <PredictionsList datas={datas.predictions} headerHeight={headerHeight} footerHeight={footerHeight}/>}
      <Header
        onLayout={(e: any) => setHeaderHeight(e.nativeEvent.layout.height)}
        title={datas?.session.name}
        subtitle={niceDatetime(datas?.session.datetime)}
        spotColor={color1}
      ></Header>
    </View>
  )
}