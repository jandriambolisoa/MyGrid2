import { useLocalSearchParams } from "expo-router"
import { useAuth } from "@/contexts/AuthContext";
import { useEffect, useState } from "react";
import { View, StyleSheet } from "react-native";
import { useApi } from "@/hooks";
import { Header, MainText, PredictionsList, Frame, ShadowButton, SpotLight } from "@/components/widgets";
import { niceDatetime } from "@/utils";
import { Constants } from "@/theme";

export default function Predictions () {

  const auth = useAuth();

  const { id, hasProno } = useLocalSearchParams();
  const { datas, error, loading, api: getPredictions } = useApi()
  const { error: makeError, loading: makeLoading, api: makePrediction } = useApi()

  const [headerHeight, setHeaderHeight] = useState(0);
  const [footerHeight, setFooterHeight] = useState(0);
  const [changed, setChanged] = useState(false);
  const [listDatas, setListDatas] = useState<any[]>([])

  useEffect(() => {
    auth && getPredictions({
      endpoint: hasProno === 'true' ? `/events/sessions/predictions/${id}` : `/events/sessions/${id}/drivers`,
      method: 'GET',
      auth: auth
    })
  }, [auth])

  useEffect(() => {
    if (hasProno === 'true') {
      if (datas?.predictions.length > 0 && !listDatas.length) {
        setListDatas(datas.predictions)
      }
    } else {
      if (datas?.drivers.length > 0 && !listDatas.length) {
        setListDatas(datas.drivers)
      }
    }
  }, [datas])

  async function handlePredictions () {
    const makeList = {
      predictions: listDatas.map((item: any, index: number) => {
        return {
          driver_id: item.driver.id,
          mygrid: index + 1
        }
      })
    }

    const response = await makePrediction({
      endpoint: `/events/sessions/predictions/${id}`,
      body: makeList,
      method: 'POST',
      auth: auth
    })
  }

  const color1 = datas?.session.event_colors[0]
  const color2 = datas?.session.event_colors.length > 0 ? datas?.session.event_colors[1] : color1

  return (
    <View style={{ flex: 1 }}>
      {listDatas?.length > 0 && <PredictionsList datas={listDatas} setDatas={setListDatas} headerHeight={headerHeight} footerHeight={footerHeight} setChanged={setChanged}/>}
      <Header
        onLayout={(e: any) => setHeaderHeight(e.nativeEvent.layout.height)}
        title={datas?.session.name}
        subtitle={niceDatetime(datas?.session.datetime)}
        spotColor={color1}
      />
      {changed && <Frame
        orientation="bottom"
        onLayout={(e: any) => setFooterHeight(e.nativeEvent.layout.height)}
      >
        <View style={[StyleSheet.absoluteFill]}>
          <SpotLight color={"#ff0000"} cx="60%" cy="60%" fx="90%" fy="90%" radius="70%" opacityStart="0.5"/>
        </View>
        <ShadowButton style={{ margin: 10 }} onPress={handlePredictions}>
          <MainText bold={true} style={{ fontSize: Constants.fontSizes.header }}>Make Prediction</MainText>
        </ShadowButton>
      </Frame>}
    </View>
  )
}