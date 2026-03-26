import { ScrollContainer, MainText, SpotLight } from "@/components/widgets";
import { Constants, GlobalStyles } from "@/theme";
import { scopedI18n } from "@/translations/i18n";
import { FlatList, View } from "react-native";

export function ChampionshipList ({
  datas=[],
  footerHeight=0,
  headerHeight=0,
  drivers=true,
}: {
  datas: any;
  footerHeight?: number;
  headerHeight?: number;
  drivers?: boolean;
}) {

  const t = scopedI18n('championship')

  function renderItem (item: any) {

    return (
      <View style={{
        paddingHorizontal: Constants.spacing.listMargin,
        paddingVertical: Constants.spacing.listMargin / 2,
        flexDirection: 'row'
      }}>
        <View style={{ alignItems: 'center', justifyContent: 'center', paddingHorizontal: Constants.spacing.listMargin, minWidth: Constants.spacing.listNumber }}>
          <MainText fontSize="header" bold={true}>{item.rank}</MainText>
        </View>
        <View style={[GlobalStyles.button, { height: Constants.spacing.userWidgetHeight, flex: 1 }]}>
          <SpotLight color={item?.team?.color} cx="60%" cy="60%" fx="80%" fy="80%" radius="70%" opacityStart="0.8" opacityEnd="0.1"/>
          <View style={{ flexDirection: 'row', paddingHorizontal: Constants.spacing.listMargin }}>
            <View style={{ flex: 1, flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', paddingStart: Constants.spacing.listMargin }}>
              <MainText bold={true} fontSize='header'>{drivers ? item?.driver?.lastname : item?.team?.name}</MainText>
              <MainText fontSize='header'>{item?.score} {t('pts')}</MainText>
            </View>
          </View>
        </View>
      </View>
    )
  }

  return (
    <ScrollContainer footerHeight={footerHeight} headerHeight={headerHeight}>
      <FlatList
        data={datas}
        renderItem={({item}) => renderItem(item)}
        scrollEnabled={false}
        contentContainerStyle={{ paddingVertical: Constants.spacing.listMargin / 2 }}
      />
    </ScrollContainer>
  )
}