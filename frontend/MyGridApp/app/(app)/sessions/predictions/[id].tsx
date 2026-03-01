import { useLocalSearchParams } from "expo-router"
import { useAuth } from "@/contexts/AuthContext";
import { useEffect, useState } from "react";
import { View } from "react-native";
import { useApi, useTimer } from "@/hooks";
import { Header, PredictionsList, PredictionsFooter } from "@/components/widgets";
import { niceDatetime } from "@/utils";
import { scopedI18n } from "@/translations/i18n";
import { DateTime } from "luxon";
import { Colors } from "@/theme";

export default function Predictions () {

  const auth = useAuth();
  const t = scopedI18n('sessions.predictions')

  const { id, hasProno, hasStarted, datetime } = useLocalSearchParams();
  const { datas, error, loading, api: getPredictions } = useApi();
  const { error: makeError, loading: makeLoading, api: makePrediction } = useApi();

  const time = useTimer(String(datetime));

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
      if (datas?.predictions?.length > 0 && !listDatas.length) {
        setListDatas(datas.predictions)
      }
    } else {
      if (datas?.drivers?.length > 0 && !listDatas.length) {
        setListDatas(datas.drivers)
      }
    }
  }, [datas])

  async function handlePredictions () {
    if (datas?.session?.datetime && DateTime.fromISO(datas.session.datetime) > DateTime.now()) {
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

      console.log(response)
    }
    console.log("Predictions can't be done after session has started")
  }

  const color1 = datas?.session?.event_colors?.[0]
  const color2 = datas?.session?.event_colors?.length > 1 ? datas.session.event_colors[1] : color1

  function potentialScore () {
    return listDatas.reduce((acc, item) => acc + (item.potential ?? 0), 0);
  }

  return (
    <View style={{ flex: 1 }}>
      {listDatas?.length > 0 && <PredictionsList
        datas={listDatas}
        setDatas={setListDatas}
        headerHeight={headerHeight}
        footerHeight={footerHeight}
        setChanged={setChanged}
        disabled={hasStarted === 'true'}
        showPotential={hasStarted === 'true' && hasProno === 'true'}
      />}
      <Header
        onLayout={(e: any) => setHeaderHeight(e.nativeEvent.layout.height)}
        title={datas?.session.name}
        subtitle={hasStarted === 'true' ? t('onGoing') : time}
        {...(hasStarted === 'true' && { subtitleColor: Colors.light.live })}
        spotColor={color1}
      />
      <PredictionsFooter
        potentialScore={potentialScore()}
        spotColor={color2}
        hasProno={hasProno === 'true'}
        hasStarted={hasStarted === 'true'}
        changed={changed}
        handlePredictions={handlePredictions}
        key={String(changed)}
        onLayout={(e: any) => setFooterHeight(e.nativeEvent.layout.height)}
      />
    </View>
  )
}