def nameTranslation(champion):                                                      # 中文化
    if champion in ["Aatrox",'aatrox','剑魔','亚托克斯','暗裔剑魔'] :
        champion = "Aatrox"
    elif champion in ['Ahri','ahri','阿狸','九尾妖狐','狐狸'] :
        champion = "Ahri"
    elif champion in ['Akali','akali','阿卡丽','离群之刺'] :
        champion = "Akali"
    elif champion in ['Alistar','alistar','牛头酋长','牛头','阿利斯塔'] :
        champion = "Alistar"
    elif champion in ['Amumu','amumu','阿木木','殇之木乃伊'] :
        champion = "Amumu"
    elif champion in ['Anivia','anivia','艾尼维亚','冰鸟','冰晶凤凰'] :
        champion = 'Anivia'
    elif champion in ['Annie','annie',"安妮",'火女',"黑暗之女"] :
        champion = 'Annie'
    elif champion in ['Ashe','ashe',"艾希","寒冰射手",'寒冰'] :
        champion = "Ashe"
    elif champion in ['Aurelion Sol','aurelion sol','Aurelionsol','aurelionsoul','奥瑞利安索尔','奥瑞利安','龙王','铸星龙王']:
        champion = "Aurelionsol"
    elif champion in ["Azir",'azir',"阿兹尔",'沙皇','沙漠皇帝',"黄鸡",'沙漠黄鸡']:
        champion  = "Azir"
    elif champion in ["Bard",'bard','巴德','星界游神']:
        champion = "Bard"
    elif champion in ['Blitzcrank','blitzcrank','布里茨','机器人','蒸汽机器人']:
        champion = 'Blitzcrank'
    elif champion in ['Brand','brand','布兰德','火男','复仇焰魂']:
        champion = 'Brand'
    elif champion in ['Braum','braum','布隆','布朗姆','弗雷尔卓德之心']:
        champion = "Braum"
    elif champion in ['Caitlyn','caitlyn','凯瑟琳','女警','皮城女警','UU']:
        champion = 'Caitlyn'
    elif champion in ['Camille','camille','卡米尔','青钢影']:
        champion = 'Camille'
    elif champion in ['Cassiopeia','cassiopeia','卡西奥佩娅','蛇女','魔蛇之拥']:
        champion = 'Cassiopeia'
    elif champion in ['Cho\'Gath','Chogath','科加斯','虚空恐惧','大虫子']:
        champion = 'Chogath'
    elif champion in ['Corki','corki','库奇','飞机','英勇投弹手']:
        champion = 'Corki'
    elif champion in ['Darius','darius','德莱厄斯','诺克萨斯之手','诺手']:
        champion = 'Darius'
    elif champion in ['Diana','diana',"戴安娜",'皎月女神','皎月']:
        champion = "Diana"
    else:
        champion = champion
        
    return champion

if __name__ == "__main__":
    nameTranslation(champion="Diana")