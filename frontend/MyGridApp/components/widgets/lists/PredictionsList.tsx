import { NumbersList, Separator, PredictionsDriverWidget } from "@/components/widgets";
import { Colors, Constants } from "@/theme";
import { Dispatch, memo, SetStateAction, useEffect, useState } from "react";
import { View, ScrollView } from "react-native";
import { GestureHandlerRootView } from 'react-native-gesture-handler'
import {
  ReorderableListReorderEvent,
  reorderItems,
  useReorderableDrag,
  NestedReorderableList,
  ScrollViewContainer
   
} from 'react-native-reorderable-list';
import { useSafeAreaInsets } from "react-native-safe-area-context";

// Override console.error
console.error = (message) => {
  if (message.includes('VirtualizedLists should never be nested inside plain ScrollViews')) {
    return;
  }
};

export type PredictionsListProps = {
  datas?: any[];
  setDatas?: Dispatch<SetStateAction<any[]>>;
  headerHeight?: number;
  footerHeight?: number;
  setChanged?: (hasChanged: boolean) => void;
}

export function PredictionsList ({
  datas=[],
  setDatas,
  headerHeight=0,
  footerHeight=0,
  setChanged
}: PredictionsListProps) {

  const CardComponent = ({ item, index }: { item: any; index: number }) => {

    const drag = useReorderableDrag();

    return (
      <PredictionsDriverWidget item={item} onLongPress={drag} delayLongPress={100}/>
    )
  };

  const Card = memo(CardComponent)

  const renderItem = ({ item, index }: { item: any; index: number}) => (
    <Card item={item} index={index} />
  )

  const handleReorder = ({from, to}: ReorderableListReorderEvent) => {
    setDatas?.((value: any) => reorderItems(value, from, to));
    setChanged?.(true)
  }

  const insets = useSafeAreaInsets();
  const paddingBottom = footerHeight ? footerHeight : insets.bottom
  const paddingTop = headerHeight ? headerHeight : insets.top

  return (
    <GestureHandlerRootView>
      <ScrollViewContainer
        style={{ backgroundColor: Colors.light.background }}
        contentContainerStyle={{ paddingBottom: paddingBottom, paddingTop: paddingTop }}
      >
        <View style={{ flexDirection: 'row', padding: Constants.spacing.listMargin }}>
          <NumbersList numbers={datas.length}/>
            <NestedReorderableList
              data={datas}
              onReorder={handleReorder}
              renderItem={renderItem}
              keyExtractor={item => item.driver.id}
              ItemSeparatorComponent={Separator as any}
              style={{ width: Constants.spacing.driverWidgetWidthWide as any}}
            />
        </View>
      </ScrollViewContainer>
    </GestureHandlerRootView>
  )
}