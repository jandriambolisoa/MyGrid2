import { useRouter } from "expo-router";
import { DateTime } from "luxon";
import { MainText, ShadowButton, Sticker } from "@/components/widgets";
import { Colors, GlobalStyles, Constants } from "@/theme";
import { View, FlatList } from "react-native";
import { scopedI18n } from "@/translations/i18n";
import { niceDatetime } from "@/utils";

export function SessionsList ({
  datas=[]
} : {
  datas?: any[];
}) {

  const router = useRouter();

  if (!datas?.length) return null;

  const t = scopedI18n('widgets.mainWidget');

  function renderItem({item} : any) {
  
    function handlePress () {

      if (!item.competitive) {
        return;
      }

      if (item.is_over) {
        if (item.has_prono) {
          router.push(`/sessions/results/${item.id}`);
          return;
        }
        
        router.push(`/sessions/resultsAlone/${item.id}`);
        return;
      }

      // Live session later
      
      router.push({
        pathname: `/sessions/predictions/${item.id}` as any,
        params: { hasProno: item.has_prono, hasStarted: String(hasStarted), datetime: item.datetime }
      })
      return;
    }

    const hasStarted = DateTime.fromISO(item.datetime) < DateTime.now()

    function rightItem () {
      if (item.is_over) {
        return (
          <MainText>{t('showResults')}</MainText>
        )
      }

      if (hasStarted) {

        if (!item.competitive && DateTime.fromISO(item.datetime).plus({ hour: 1 }) < DateTime.now()) {
          return (
            <MainText>{t('finished')}</MainText>
          )
        }
        return (
          <MainText style={{ color: Colors.light.live }}>{t('onGoing')}</MainText>
        )
      }

      return (
        <MainText>{niceDatetime(item.datetime)}</MainText>
      )
    }

    return(
      <View style={{ overflow: 'hidden', marginBottom: Constants.spacing.buttonPadding }}>
        <ShadowButton
          innerStyle={[GlobalStyles.mainWidgetButton]}
          style={{ overflow: "visible" }}
          onPress={handlePress}
          absoluteChild={item.has_prono && <Sticker style={{ left: '30%' }}/>}
        >
          <MainText>{item.name}</MainText>
          {rightItem()}
        </ShadowButton>
      </View>
    )
  }

  return (
    <FlatList
      data={datas}
      renderItem={renderItem}
      showsVerticalScrollIndicator={false}
      style={{ alignSelf: "stretch" }}
    />
  )
}