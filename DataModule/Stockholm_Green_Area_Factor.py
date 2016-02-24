
class Module_SGAF:
    """
        class for getting data for Stockholm Green Area Factory Module
    """
    def __init__(self, postresDataManager, schema_id):
        self.schemaID = schema_id
        self._pdm = postresDataManager
        self.responseData = {}

    # todo TEST SCHEMA VALID FOR SQL INJECTION !!
    def _get_generic_count_attribute(self, filtered_class):
        request = """SELECT COUNT(attr_gml_id) FROM {}.gen_genericcityobject
                    WHERE gen_class='{}';""".format(self.schemaID, filtered_class)
        return self._pdm.getDataValue(request, int)

    def _get_bird_feeder_experential(self):
        request = """SELECT COUNT(attr_gml_id) FROM {}.gen_genericcityobject
                      WHERE gen_class='ECD_GENCO_BIRD_FEEDER' AND attr_gml_id IN (
                        SELECT parentfk FROM {}.gen_genericcityobject_gen_intattribute
                          WHERE attr_name='isExperiential' AND gen_value=1
                    );""".format(self.schemaID, self.schemaID)
        return self._pdm.getDataValue(request, int)

    def _get_impermeable_surfaces(self):
        request = """SELECT COUNT(attr_gml_id) FROM {}.luse_landuse
                      WHERE attr_gml_id IN (
                        SELECT parentfk FROM {}.luse_landuse_gen_intattribute
                          WHERE attr_name='isPermeable' AND gen_value=0
                    );""".format(self.schemaID, self.schemaID)
        return self._pdm.getDataValue(request, int)

    def _get_count_tree_with_trunk_parameter(self, minDiameter, maxDiameter):
        request = """SELECT COUNT(*) FROM {}.veg_solitaryvegetationobject
                      WHERE veg_trunkdiameter_attr_uom='#cm' AND veg_trunkdiameter >= {} AND veg_trunkdiameter <= {};
                  """.format(self.schemaID, minDiameter, maxDiameter)
        return self._pdm.getDataValue(request, int)

    def _get_count_oaks(self):
        request = """SELECT COUNT(attr_gml_id) FROM {}.veg_solitaryvegetationobject
                    WHERE veg_class='ECD_SOLVEG_OAK';""".format(self.schemaID)
        return self._pdm.getDataValue(request, int)

    def _get_count_vegetary_attribute(self, filtered_class):
        request = """SELECT COUNT(attr_gml_id) FROM {}.veg_solitaryvegetationobject
                      WHERE attr_gml_id IN (
                        SELECT parentfk FROM {}.veg_solitaryvegetationobject_gen_intattribute
                          WHERE attr_name='{}' AND gen_value=1
                  );""".format(self.schemaID, self.schemaID, filtered_class)
        return self._pdm.getDataValue(request, int)

    def _get_count_fruit_blooming_attribute(self):
        request = """SELECT COUNT(attr_gml_id) FROM {}.veg_solitaryvegetationobject
                      WHERE attr_gml_id IN (
                        SELECT parentfk FROM (
                          SELECT parentfk FROM {}.veg_solitaryvegetationobject_gen_intattribute
                            WHERE attr_name='isBlooming' AND gen_value=1 UNION SELECT parentfk FROM {}.veg_solitaryvegetationobject_gen_intattribute
                              WHERE attr_name='isFruit' AND gen_value=1
                          ) AS INTERMEDIATE GROUP BY parentfk HAVING count(parentfk) > 0
                      );""".format(self.schemaID, self.schemaID, self.schemaID)
        return self._pdm.getDataValue(request, int)

    def _get_count_water_filtered_name(self, filtered_name):
        request = """SELECT COUNT(attr_gml_id) FROM {}.wtr_watersurface
                      WHERE attr_gml_id IN (
                        SELECT parentfk FROM {}.wtr_watersurface_gen_intattribute
                          WHERE attr_name='' AND gen_value=1
                  );""".format(self.schemaID, self.schemaID, filtered_name)
        return self._pdm.getDataValue(request, int)

    def _get_count_filtered_fountains(self, filtered_name):
        request = """SELECT COUNT(attr_gml_id) FROM {}.wtr_watersurface
                      WHERE wtr_class='1230' AND attr_gml_id IN (
                        SELECT parentfk FROM {}.wtr_watersurface_gen_intattribute
                          WHERE attr_name='{}' AND gen_value=1
                  );""".format(self.schemaID, self.schemaID, filtered_name)
        return self._pdm.getDataValue(request, int)


    def _get_generic_sum_attribute(self, filtered_class):
        request = """SELECT SUM(gen_value) FROM {}.gen_genericcityobject_gen_doubleattribute
                    WHERE attr_name='area' AND parentfk IN (
                      SELECT attr_gml_id FROM {}.gen_genericcityobject WHERE gen_class='{}'
                  );""".format(self.schemaID, self.schemaID, filtered_class)
        return self._pdm.getDataValue(request, float)

    def _get_balcony_terrace_growing(self):
        request ="""SELECT SUM(gen_value) FROM {}.gen_genericcityobject_gen_doubleattribute
                      WHERE attr_name='area' AND gen_value>0 AND parentfk IN (
                        SELECT parentfk FROM ( {}.gen_genericcityobject_gen_intattribute
                          WHERE attr_name='isBalconyTerraceForGrowing' AND gen_value=1
                  );""".format(self.schemaID, self.schemaID)
        return self._pdm.getDataValue(request, float)

    def _get_runoff_surfaces(self):
        request ="""SELECT SUM(gen_value) FROM {}.gen_genericcityobject_gen_doubleattribute
                      WHERE attr_name='area' AND gen_value>0 AND parentfk IN (
                        SELECT parentfk FROM {}.gen_genericcityobject_gen_intattribute
                          WHERE attr_name='isRunoffFromImpermeableToVegetated' AND gen_value=1
                        ) AS INTERMEDIATE GROUP BY parentfk HAVING count(parentfk) = 1
                  );""".format(self.schemaID, self.schemaID)
        return self._pdm.getDataValue(request, float)

    def _get_general_bushes(self):
        request = """SELECT SUM(gen_value) FROM {}.gen_genericcityobject_gen_doubleattribute
                    WHERE attr_name='area' AND parentfk IN (
                      SELECT attr_gml_id FROM {}.veg_plantcover WHERE veg_class='1080'
                  );""".format(self.schemaID, self.schemaID)
        return self._pdm.getDataValue(request, float)

    def _get_total_land_area(self, filtered_name):
        request = """SELECT SUM(gen_value) total_land_area FROM {}.luse_landuse_gen_doubleattribute
                      WHERE attr_name='area' AND  gen_value>0 AND parentfk IN (
                        SELECT parentfk FROM {}.luse_landuse_gen_intattribute
                        WHERE attr_name='{}' AND gen_value=1 );""".format(self.schemaID, self.schemaID, filtered_name)
        return self._pdm.getDataValue(request, float)

    def _get_landuse_sum_doubled_filtered(self, filtered_anme_1, filtered_name_2):
        request = """SELECT SUM(gen_value) FROM {}.luse_landuse_gen_doubleattribute
                       WHERE attr_name='area' AND gen_value>0 AND parentfk IN (
                        SELECT parentfk FROM (
                          SELECT * FROM {}.luse_landuse_gen_intattribute
                            WHERE attr_name='{}' AND gen_value=1 UNION
                              SELECT * FROM {}.luse_landuse_gen_intattribute
                                WHERE attr_name='isOpenHard' AND gen_value=1
                          ) AS INTERMEDIATE GROUP BY parentfk HAVING count(parentfk) = 2
                    );""".format(self.schemaID, self.schemaID, filtered_anme_1, self.schemaID, filtered_name_2)
        return self._pdm.getDataValue(request, float)

    def _get_concrete_slabs(self):
        request = """SELECT SUM(gen_value) FROM {}.luse_landuse_gen_doubleattribute
                      WHERE attr_name='area' AND gen_value>0 AND parentfk IN (
                        SELECT parentfk FROM (
                          SELECT * FROM {}.luse_landuse_gen_intattribute
                            WHERE attr_name='isConcrete' AND gen_value=1
                        ) AS INTERMEDIATE GROUP BY parentfk HAVING count(parentfk) = 1
                      );""".format(self.schemaID, self.schemaID)
        return self._pdm.getDataValue(request, float)

    def _get_dry_areas(self):
        request = """SELECT SUM(gen_value) Sum_areas_dr FROM {}.luse_landuse_gen_doubleattribute
                      WHERE attr_name='area' AND gen_value>0 AND parentfk IN (
                        SELECT parentfk FROM (
                          SELECT * FROM {}.luse_landuse_gen_intattribute
                            WHERE attr_name='isDry' AND gen_value=1 UNION
                             SELECT * FROM {}.luse_landuse_gen_intattribute
                              WHERE attr_name='isWithPlants' AND gen_value=1 UNION
                                SELECT * FROM {}.luse_landuse_gen_intattribute
                                  WHERE attr_name='isFilledWithRainWater' AND gen_value=1
                          ) AS DRY_AREAS_WITH_PLANTS_FILL_WITH_RAIN_WATER GROUP BY parentfk HAVING count(parentfk) = 3
                    );""".format(self.schemaID, self.schemaID, self.schemaID, self.schemaID)
        return self._pdm.getDataValue(request, float)

    def _get_unsupported_ground_greenery(self):
        request = """SELECT SUM(gen_value) FROM {}.veg_plantcover_gen_doubleattribute
                      WHERE attr_name='area' AND gen_value>0 AND parentfk IN (
                        SELECT parentfk FROM (
                          SELECT * FROM {}.veg_plantcover_gen_intattribute
                          WHERE attr_name='isUnsupported' AND gen_value=1 UNION
                          SELECT * FROM {}.veg_plantcover_gen_intattribute
                          WHERE attr_name='isOnGround' AND gen_value=1
                          ) AS AN_ALIAS GROUP BY parentfk HAVING count(parentfk) = 2
                      ); """.format(self.schemaID, self.schemaID, self.schemaID)
        return self._pdm.getDataValue(request, float)

    def _get_plant_bed_with_height(self, minHeight, maxHeight):
        request = """SELECT SUM(gen_value) FROM {}.veg_plantcover_gen_doubleattribute
                      WHERE attr_name='area' AND gen_value>0 AND parentfk IN (
                        SELECT attr_gml_id FROM {}.veg_plantcover INNER JOIN
                        {}.veg_plantcover_gen_intattribute ON {}.veg_plantcover.attr_gml_id = {}.veg_plantcover_gen_intattribute.parentfk
                        WHERE attr_name='isOnGround' AND gen_value=1 AND veg_averageheight > {} AND veg_averageheight < {}
                      );""".format(self.schemaID, self.schemaID, self.schemaID, self.schemaID, self.schemaID, minHeight, maxHeight)
        return self._pdm.getDataValue(request, float)

    def _get_green_roof(self, minHeight, maxHeight):
        request = """SELECT SUM(gen_value) FROM {}.veg_plantcover_gen_doubleattribute
                      WHERE attr_name='area' AND parentfk IN (
                        SELECT attr_gml_id FROM {}.veg_plantcover INNER JOIN
                          {}.veg_plantcover_gen_intattribute ON {}.veg_plantcover.attr_gml_id ={}.veg_plantcover_gen_intattribute.parentfk
                          WHERE attr_name='isOnRoof' AND gen_value=1 AND veg_averageheight > {} AND veg_averageheight < {}
                      );""".format(self.schemaID, self.schemaID, self.schemaID, self.schemaID, self.schemaID, minHeight, maxHeight)
        return self._pdm.getDataValue(request, float)

    def _get_sum_vegetation_filtered(self, filtered_name):
        request = """SELECT SUM(gen_value) FROM {}.veg_plantcover_gen_doubleattribute
                      WHERE attr_name='area' AND gen_value>0 AND parentfk IN (
                        SELECT parentfk FROM {}.veg_plantcover_gen_intattribute
                          WHERE attr_name='{}' AND gen_value=1
                  );""".format(self.schemaID, self.schemaID, filtered_name)
        return self._pdm.getDataValue(request, float)

    def _get_sum_vegetation_join_name_filtered(self, filtered_class):
        request = """SELECT SUM(gen_value) FROM {}.veg_plantcover_gen_doubleattribute
                      WHERE attr_name='area' AND parentfk IN (
                        SELECT attr_gml_id FROM {}.veg_plantcover INNER JOIN {}.veg_plantcover_gen_intattribute
                          ON {}.veg_plantcover.attr_gml_id = {}.veg_plantcover_gen_intattribute.parentfk
                            WHERE attr_name='{}' AND gen_value=1
                  )""".format(self.schemaID, self.schemaID, self.schemaID, self.schemaID, self.schemaID, filtered_class)
        return self._pdm.getDataValue(request, float)

    def _get_grass_ball_games(self):
        request = """SELECT SUM(gen_value) FROM {}.veg_plantcover_gen_doubleattribute
                      WHERE attr_name='area' AND parentfk IN (
                        SELECT attr_gml_id FROM {}.veg_plantcover INNER JOIN {}.veg_plantcover_gen_intattribute ON {}.veg_plantcover.attr_gml_id = {}.veg_plantcover_gen_intattribute.parentfk
                         WHERE attr_name='isPlayable' AND gen_value=1 AND veg_class='1040'
                  )""".format(self.schemaID, self.schemaID, self.schemaID, self.schemaID, self.schemaID)
        return self._pdm.getDataValue(request, float)

    def _get_gardening_in_yards(self):
        request ="""SELECT SUM(gen_value) FROM {}.veg_plantcover_gen_doubleattribute
                    WHERE attr_name='area' AND gen_value>0 AND parentfk IN (
                      SELECT parentfk FROM (
                        SELECT * FROM {}.veg_plantcover_gen_intattribute
                          WHERE attr_name='isGardening' AND gen_value=1 UNION
                            SELECT * FROM {}.veg_plantcover_gen_intattribute
                              WHERE attr_name='isInYard' AND gen_value=1
                          ) AS INTERMEDIATE GROUP BY parentfk HAVING count(parentfk) = 2
                  );""".format(self.schemaID, self.schemaID, self.schemaID)
        return self._pdm.getDataValue(request, float)

    def _get_visible_green(self):
        request ="""SELECT SUM(gen_value) FROM {}.veg_plantcover_gen_doubleattribute
                      WHERE attr_name='area' AND gen_value>0 AND parentfk IN (
                        SELECT parentfk FROM (
                          SELECT * FROM {}.veg_plantcover_gen_intattribute
                            WHERE attr_name='isVisible' AND gen_value=1 UNION
                              SELECT * FROM {}.veg_plantcover_gen_intattribute
                                WHERE attr_name='isOnRoof' AND gen_value=1
                      ) AS INTERMEDIATE GROUP BY parentfk HAVING count(parentfk) = 2
                  );""".format(self.schemaID, self.schemaID, self.schemaID)
        return self._pdm.getDataValue(request, float)

    def _get_floral_arrangement(self):
        request ="""SELECT SUM(gen_value) FROM {}.veg_plantcover_gen_doubleattribute
                      WHERE attr_name='area' AND parentfk IN (
                        SELECT attr_gml_id FROM {}.veg_plantcover WHERE veg_class='ECD_VEG_FLORAL_ARRANGEMENT'
                  );""".format(self.schemaID, self.schemaID)
        return self._pdm.getDataValue(request, float)

    def _get_sum_bushes(self, filtered_class):
        request ="""SELECT SUM(gen_value) FROM {}.veg_plantcover_gen_doubleattribute
                      WHERE attr_name='area' AND parentfk IN (
                        SELECT attr_gml_id FROM {}.veg_plantcover INNER JOIN {}.veg_plantcover_gen_intattribute ON
                          {}.veg_plantcover.attr_gml_id = {}.veg_plantcover_gen_intattribute.parentfk
                            WHERE attr_name='{}' AND gen_value=1 AND veg_class='1080'
                  );""".format(self.schemaID, self.schemaID, self.schemaID, self.schemaID, self.schemaID, filtered_class)
        return self._pdm.getDataValue(request, float)

    def _get_sum_water_body_filtered(self, filtered_name):
        request ="""SELECT SUM(gen_value) FROM {}.wtr_waterbody_gen_doubleattribute
                      WHERE attr_name='area' AND gen_value>0 AND parentfk IN (
                        SELECT parentfk FROM (
                          SELECT * FROM {}.wtr_waterbody_gen_intattribute
                            WHERE attr_name='{}' AND gen_value=1
                        ) AS INTERMEDIATE GROUP BY parentfk HAVING count(parentfk) = 1
                  );""".format(self.schemaID, self.schemaID, filtered_name)
        return self._pdm.getDataValue(request, float)

    def _get_green_water_surfaces(self):
        request ="""SELECT SUM(gen_value) FROM {}.wtr_waterbody_gen_doubleattribute
                      WHERE attr_name='area' AND parentfk IN (
                        SELECT attr_gml_id FROM {}.wtr_waterbody_gen_intattribute
                     );""".format(self.schemaID, self.schemaID)
        return self._pdm.getDataValue(request, float)

    def _get_biologically_accessible_water(self):
        request ="""SELECT SUM(gen_value) FROM {}.wtr_watersurface_gen_doubleattribute
                      WHERE attr_name='area' AND gen_value>0 AND parentfk IN (
                        SELECT parentfk FROM (
                          SELECT * FROM {}.wtr_watersurface_gen_intattribute
                            WHERE attr_name='isExperiential' AND gen_value=1 UNION
                              SELECT * FROM {}.wtr_watersurface_gen_intattribute
                                WHERE attr_name='isBiologicallyAccessible' AND gen_value=1
                        ) AS INTERMEDIATE GROUP BY parentfk HAVING count(parentfk) = 2
                    );""".format(self.schemaID, self.schemaID, self.schemaID)
        return self._pdm.getDataValue(request, float)


    def getData(self):
        self.responseData["Total land area"] = self._get_total_land_area('isCaseStudyDistrict')

        self.responseData["Unsupported ground greenery"] = self._get_unsupported_ground_greenery()
        self.responseData["Plant bed (>800 mm)"] = self._get_plant_bed_with_height(800, 100000)
        self.responseData["Plant bed (600 - 800 mm)"] = self._get_plant_bed_with_height(600, 800)
        self.responseData["Plant bed (200 - 600 mm)"] = self._get_plant_bed_with_height(200, 600)
        self.responseData["Green roof (>300 mm)"] = self._get_green_roof(300, 100000)
        self.responseData["Green roof (50 - 300 mm)"] = self._get_green_roof(50, 300)
        self.responseData["Greenery on walls"] = self._get_sum_vegetation_filtered('isOnWall')
        self.responseData["Balcony boxes"] = self._get_generic_count_attribute('ECD_GENCO_BALCONY_BOX')

        self.responseData['Diversity in the field layer'] = self._get_generic_sum_attribute('ECD_GENCO_DIVERSITY_FIELD_LAYER')
        self.responseData['Natural species selection'] = self._get_generic_sum_attribute('ECD_GENCO_NATURAL_SPECIES_SELECTION')
        self.responseData['Diversity on thin sedum roofs'] = self._get_generic_sum_attribute('ECD_GENCO_DIVERSITY_THIN_SEDUM_ROOF')
        self.responseData['Integrated balcony boxes with climbing plants'] = self._get_generic_sum_attribute('ECD_GENCO_INTEGRATED_BALCONY_BOX_CLIMBING')
        self.responseData['Butterfly restaurants'] = self._get_generic_count_attribute('ECD_GENCO_BUTTERFLY_RESTAURANT')
        self.responseData['General bushes'] = self._get_general_bushes()
        self.responseData['Berry bushes'] = self._get_sum_vegetation_join_name_filtered('isBerry')
        self.responseData['Large trees'] = self._get_count_tree_with_trunk_parameter(30, 100000)
        self.responseData['Medium large trees'] = self._get_count_tree_with_trunk_parameter(20, 30)
        self.responseData['Small trees'] = self._get_count_tree_with_trunk_parameter(16, 20)
        self.responseData['Oaks'] = self._get_count_oaks()
        self.responseData['Fruit trees'] = self._get_count_vegetary_attribute('isFruit')
        self.responseData['Fauna depots'] = self._get_generic_count_attribute('ECD_GENCO_FAUNA_DEPOT')
        self.responseData['Beetle feeders'] = self._get_generic_count_attribute('ECD_GENCO_BEETLE_FEEDER')
        self.responseData['Bird feeders'] = self._get_generic_count_attribute('ECD_GENCO_BIRD_FEEDER')

        self.responseData['Grass area games'] = self._get_grass_ball_games()
        self.responseData['Gardening areas in yards'] = self._get_gardening_in_yards()
        self.responseData['Balconies and terraces prepared for growing'] = self._get_balcony_terrace_growing()
        self.responseData['Shared roof terraces'] = self._get_sum_water_body_filtered('isSharedRoofTerrace')
        self.responseData['Visible green roofs'] = self._get_visible_green()
        self.responseData['Floral arrangements'] = self._get_floral_arrangement()
        self.responseData['Experiential values of bushes'] = self._get_sum_bushes('isExperiential')
        self.responseData['Berry bushes with edible fruits'] = self._get_sum_bushes('isBerry')
        self.responseData['Trees experiential value'] = self._get_count_vegetary_attribute('isExperiential')
        self.responseData['Fruit trees and blooming trees'] = self._get_count_fruit_blooming_attribute()
        self.responseData['Green surrounded'] = self._get_total_land_area('isGreenSurrounded')
        self.responseData['Bird feeders experiential value'] = self._get_bird_feeder_experential()

        self.responseData['Trees leafy shading'] = self._get_count_vegetary_attribute('isLeafyShading')
        self.responseData['Shade from leaf cover'] = self._get_sum_vegetation_join_name_filtered('isShadeFromLeaf')
        self.responseData['Evening out of temp'] = self._get_sum_vegetation_filtered('isEveningOutOfTemp')

        self.responseData['Water surface permanent'] = self._get_count_water_filtered_name('isPermanent')
        self.responseData['Open hard surfaces that allow water to get through'] = self._get_landuse_sum_doubled_filtered('isPermeable', 'isOpenHard')
        self.responseData['Gravel and sand'] = self._get_landuse_sum_doubled_filtered('isGravel', 'isSand')
        self.responseData['Concrete slabs with joints'] = self._get_concrete_slabs()
        self.responseData['Impermeable surfaces'] = self._get_impermeable_surfaces()

        self.responseData['Biologically accessible permanent water'] = self._get_sum_water_body_filtered('isPermanent')
        self.responseData['Dry areas with plants that temporarily fill with rain water'] = self._get_dry_areas()
        self.responseData['Delay of rainwater in ponds'] = self._get_sum_water_body_filtered('isRainwaterDelayedInPonds')
        self.responseData['Delay of rainwater in underground percolation systems'] = self._get_sum_water_body_filtered('isRainwaterDelayedInPercolationsystems')
        self.responseData['Runoff from impermeable surfaces to surfaces with plants'] = self._get_balcony_terrace_growing()

        self.responseData['Water surfaces'] = self._get_green_water_surfaces()
        self.responseData['Biologically accessible water'] = self._get_biologically_accessible_water()
        self.responseData['Fountains circulations systems'] = self._get_count_filtered_fountains('isCirculationSystem')

        self.responseData['Water collection during dry periods'] = self._get_count_water_filtered_name('isCollectedDuringDryPeriods')
        self.responseData['Collected rainwater for watering'] = self._get_count_water_filtered_name('isForWatering')
        self.responseData['Fountains cooling effect'] = self._get_count_filtered_fountains('isCooling')

        return self.responseData
