import { useLocalSearchParams, useRouter } from "expo-router"
import { useAuth } from "@/contexts/AuthContext";
import { useEffect, useState } from "react";
import { ActivityIndicator, View } from "react-native";
import { useApi, useTimer } from "@/hooks";
import { Header, PredictionsList, PredictionsFooter, ListsLabels } from "@/components/widgets";
import { scopedI18n } from "@/translations/i18n";
import { DateTime } from "luxon";
import { Colors } from "@/theme";

export default function Predictions () {

  const auth = useAuth();
  const t = scopedI18n('sessions.predictions');
  const router = useRouter();

  const { id, hasProno, hasStarted, datetime } = useLocalSearchParams();
  const { datas, error, loading, api: getPredictions } = useApi(true);
  const { error: makeError, status: makeStatus, loading: makeLoading, api: makePrediction } = useApi();
  const { datas: paramsDatas, api: getParams } = useApi();

  const time = useTimer(String(datetime));

  const [headerHeight, setHeaderHeight] = useState(0);
  const [footerHeight, setFooterHeight] = useState(0);
  const [changed, setChanged] = useState(false);
  const [listDatas, setListDatas] = useState<any[]>([]);

  useEffect(() => {
    auth && getPredictions({
      endpoint: `/events/sessions/${id}/drivers`,
      method: 'GET',
      auth: auth
    });
  }, [auth]);

  useEffect(() => {
    if (hasProno === 'true' || hasStarted === 'false') {
      auth && !loading && getParams({
        endpoint: `/scores/parameters/1`,
        method: 'GET',
        auth: auth
      });
    }
  }, [loading]);

  useEffect(() => {
      if (datas?.drivers?.length > 0 && !listDatas.length) {
        if (hasProno === 'false' && hasStarted === 'false') {
          const newDatas = datas.drivers.map((item: any, index: number) => ({
            ...item,
            mygrid: index + 1
          }))
          setListDatas(newDatas);
        } else {
          setListDatas(datas.drivers);
        }
      }
  }, [datas]);

  useEffect(() => {
      if (makeStatus === 403) {
        router.push('/verify/resend')
      }
  }, [makeStatus])

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

      const success = await makePrediction({
        endpoint: `/events/sessions/predictions/${id}`,
        body: makeList,
        method: 'POST',
        auth: auth
      })

      if (success) {
        router.back()
      }
      return
    }
    // Should be removed
    console.log("Predictions can't be done after session has started")
  }

  const color1 = datas?.session?.event_colors?.[0]
  const color2 = datas?.session?.event_colors?.length > 1 ? datas.session.event_colors[1] : color1

  return (
    <View style={{ flex: 1, backgroundColor: Colors.light.background, justifyContent: 'center' }}>
      {loading && <ActivityIndicator color={Colors.light.orangeLogo}/>}
      {listDatas?.length > 0 && <PredictionsList
        datas={listDatas}
        setDatas={setListDatas}
        headerHeight={headerHeight}
        footerHeight={footerHeight}
        setChanged={setChanged}
        disabled={hasStarted === 'true'}
        parameters={paramsDatas}
      />}
      <Header
        onLayout={(e: any) => setHeaderHeight(e.nativeEvent.layout.height)}
        title={datas?.session.name}
        subtitle={hasStarted === 'true' ? t('onGoing') : time}
        {...(hasStarted === 'true' && { subtitleColor: Colors.light.live })}
        spotColor={color1}
      >
        <ListsLabels points={hasProno === 'true' || hasStarted === 'false'} noGrid={hasStarted === 'true' && hasProno === 'false'}/>
      </Header>
      {changed && <PredictionsFooter
        spotColor={color2}
        handlePredictions={handlePredictions}
        onLayout={(e: any) => setFooterHeight(e.nativeEvent.layout.height)}
        loading={makeLoading}
      />}
    </View>
  )
}