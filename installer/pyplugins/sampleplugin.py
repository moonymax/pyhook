plugin = None


def onEnable(**kwargs):  # is called when the connection to java was established
    global plugin
    plugin = kwargs['plugin']
    plugin.registerCommand("test", "Usage: /test",
                           "Description: This is a test command", "test.command", None)
    plugin.registerCommand("test2", None, None, None, None)

    print('hello from sampleplugin.py')


def onTest2Cmd(**kwargs):
    plugin = kwargs['plugin']
    sender = kwargs['sender']
    name = kwargs['name']
    arguments = kwargs['arguments']
    for arg in arguments:
        print('argument:', arg)


def onTestCmd(**kwargs):
    plugin = kwargs['plugin']
    sender = kwargs['sender']
    name = kwargs['name']
    arguments = kwargs['arguments']
    print('a command was run')
    print('sender:', sender.getDisplayName())


"""
BlockBreakEvent,
BlockBurnEvent,
BlockCanBuildEvent,
BlockDamageEvent,
BlockDispenseEvent,
BlockExpEvent,
BlockExplodeEvent,
BlockFadeEvent,
BlockFormEvent,
BlockFromToEvent,
BlockGrowEvent,
BlockIgniteEvent,
BlockMultiPlaceEvent,
BlockPhysicsEvent,
BlockPistonExtendEvent,
BlockPistonRetractEvent,
BlockPlaceEvent,
BlockRedstoneEvent,
BlockSpreadEvent,
EntityBlockFormEvent,
LeavesDecayEvent,
NotePlayEvent,
SignChangeEvent,
EnchantItemEvent,
PrepareItemEnchantEvent,
CreatureSpawnEvent,
CreeperPowerEvent,
EntityBreakDoorEvent,
EntityChangeBlockEvent,
EntityCombustByBlockEvent,
EntityCombustByEntityEvent,
EntityCombustEvent,
EntityCreatePortalEvent,
EntityDamageByBlockEvent,
EntityDamageByEntityEvent,
EntityDamageEvent,
EntityDeathEvent,
EntityExplodeEvent,
EntityInteractEvent,
EntityPortalEnterEvent,
EntityPortalEvent,
EntityPortalExitEvent,
EntityRegainHealthEvent,
EntityShootBowEvent,
EntitySpawnEvent,
EntityTameEvent,
EntityTargetEvent,
EntityTargetLivingEntityEvent,
EntityTeleportEvent,
EntityUnleashEvent,
ExpBottleEvent,
ExplosionPrimeEvent,
FireworkExplodeEvent,
FoodLevelChangeEvent,
HorseJumpEvent,
ItemDespawnEvent,
ItemMergeEvent,
ItemSpawnEvent,
PigZapEvent,
PlayerDeathEvent,
PlayerLeashEntityEvent,
PotionSplashEvent,
ProjectileHitEvent,
ProjectileLaunchEvent,
SheepDyeWoolEvent,
SheepRegrowWoolEvent,
SlimeSplitEvent,
SpawnerSpawnEvent,
HangingBreakByEntityEvent,
HangingBreakEvent,
HangingPlaceEvent,
BrewEvent,
CraftItemEvent,
FurnaceBurnEvent,
FurnaceExtractEvent,
FurnaceSmeltEvent,
InventoryClickEvent,
InventoryCloseEvent,
InventoryCreativeEvent,
InventoryDragEvent,
InventoryEvent,
InventoryMoveItemEvent,
InventoryOpenEvent,
InventoryPickupItemEvent,
PrepareItemCraftEvent,
PaintingBreakByEntityEvent,
PaintingBreakEvent,
PaintingPlaceEvent,
AsyncPlayerChatEvent,
AsyncPlayerPreLoginEvent,
PlayerAchievementAwardedEvent,
PlayerAnimationEvent,
PlayerArmorStandManipulateEvent,
PlayerBedEnterEvent,
PlayerBedLeaveEvent,
PlayerBucketEmptyEvent,
PlayerBucketFillEvent,
PlayerChangedWorldEvent,
PlayerChatEvent,
PlayerChatTabCompleteEvent,
PlayerCommandPreprocessEvent,
PlayerDropItemEvent,
PlayerEditBookEvent,
PlayerEggThrowEvent,
PlayerExpChangeEvent,
PlayerFishEvent,
PlayerGameModeChangeEvent,
PlayerInteractAtEntityEvent,
PlayerInteractEntityEvent,
PlayerInteractEvent,
PlayerInventoryEvent,
PlayerItemBreakEvent,
PlayerItemConsumeEvent,
PlayerItemDamageEvent,
PlayerItemHeldEvent,
PlayerJoinEvent,
PlayerKickEvent,
PlayerLevelChangeEvent,
PlayerLoginEvent,
PlayerMoveEvent,
PlayerPickupItemEvent,
PlayerPortalEvent,
PlayerPreLoginEvent,
PlayerQuitEvent,
PlayerRegisterChannelEvent,
PlayerResourcePackStatusEvent,
PlayerRespawnEvent,
PlayerShearEntityEvent,
PlayerStatisticIncrementEvent,
PlayerTeleportEvent,
PlayerToggleFlightEvent,
PlayerToggleSneakEvent,
PlayerToggleSprintEvent,
PlayerUnleashEntityEvent,
PlayerUnregisterChannelEvent,
PlayerVelocityEvent,
MapInitializeEvent,
PluginDisableEvent,
PluginEnableEvent,
RemoteServerCommandEvent,
ServerCommandEvent,
ServerListPingEvent,
ServiceRegisterEvent,
ServiceUnregisterEvent,
VehicleBlockCollisionEvent,
VehicleCreateEvent,
VehicleDamageEvent,
VehicleDestroyEvent,
VehicleEnterEvent,
VehicleEntityCollisionEvent,
VehicleExitEvent,
VehicleMoveEvent,
VehicleUpdateEvent,
LightningStrikeEvent,
ThunderChangeEvent,
WeatherChangeEvent,
ChunkLoadEvent,
ChunkPopulateEvent,
ChunkUnloadEvent,
PortalCreateEvent,
SpawnChangeEvent,
StructureGrowEvent,
WorldInitEvent,
WorldLoadEvent,
WorldSaveEvent,
WorldUnloadEvent,
EntityDismountEvent,
EntityMountEvent,
PlayerSpawnLocationEvent
"""
