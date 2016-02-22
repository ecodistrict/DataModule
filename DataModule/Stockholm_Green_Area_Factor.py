
class Module_SGAF:
    """
        class for getting data for Stockholm Green Area Factory Module
    """
    def __init__(self, postresDataManager, caseID, varID):
        self.schemaID = caseID + "_" + varID
        self._pdm = postresDataManager
        self.responseData = {}

    # todo TEST SCHEMA VALID FOR SQL INJECTION !!

    def _get_total_land_area(self):
        request = """SELECT SUM(gen_value) total_land_area FROM {}.luse_landuse_gen_doubleattribute
                      WHERE attr_name='area' AND  gen_value>0 AND parentfk IN (
                        SELECT parentfk FROM {}.luse_landuse_gen_intattribute
                        WHERE attr_name='isCaseStudyDistrict' AND gen_value=1 );""".format(self.schemaID, self.schemaID)
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
        return self._pdm.getDataValue(request, int)

    def _get_green_roof(self, minHeight, maxHeight):
        request = """SELECT SUM(gen_value) FROM {}.veg_plantcover_gen_doubleattribute
                      WHERE attr_name='area' AND parentfk IN (
                        SELECT attr_gml_id FROM {}.veg_plantcover INNER JOIN
                          {}.veg_plantcover_gen_intattribute ON {}.veg_plantcover.attr_gml_id ={}.veg_plantcover_gen_intattribute.parentfk
                          WHERE attr_name='isOnRoof' AND gen_value=1 AND veg_averageheight > {} AND veg_averageheight < {}
                      );""".format(self.schemaID, self.schemaID, self.schemaID, self.schemaID, self.schemaID, minHeight, maxHeight)
        return self._pdm.getDataValue(request, float)

    def _get_green_on_walls(self):
        request = """SELECT SUM(gen_value) FROM {}.veg_plantcover_gen_doubleattribute
                  WHERE attr_name='area' AND gen_value>0 AND parentfk IN (
                    SELECT parentfk FROM {}.veg_plantcover_gen_intattribute
                      WHERE attr_name='isOnWall' AND gen_value=1
                  );""".format(self.schemaID, self.schemaID)
        return self._pdm.getDataValue(request, float)

    def _get_generic_count_attribute(self, filtered_class):
        request = """SELECT COUNT(attr_gml_id) FROM {}.gen_genericcityobject
                    WHERE gen_class='{}';""".format(self.schemaID, filtered_class)
        return self._pdm.getDataValue(request, int)

    def _get_generic_sum_attribute(self, filtered_class):
        request = """SELECT SUM(gen_value) FROM {}.gen_genericcityobject_gen_doubleattribute
                    WHERE attr_name='area' AND parentfk IN (
                      SELECT attr_gml_id FROM {}.gen_genericcityobject WHERE gen_class='{}'
                  );""".format(self.schemaID, self.schemaID, filtered_class)
        return self._pdm.getDataValue(request, float)

    def _get_general_bushes(self):
        request = """SELECT SUM(gen_value) FROM {}.gen_genericcityobject_gen_doubleattribute
                    WHERE attr_name='area' AND parentfk IN (
                      SELECT attr_gml_id FROM {}.veg_plantcover WHERE veg_class='1080'
                  );""".format(self.schemaID, self.schemaID)
        return self._pdm.getDataValue(request, float)

    def _get_berry_bushes(self):
        request = """SELECT SUM(gen_value) FROM {}.veg_plantcover_gen_doubleattribute
                      WHERE attr_name='area' AND parentfk IN (
                        SELECT attr_gml_id FROM {}.veg_plantcover INNER JOIN
                          {}.veg_plantcover_gen_intattribute ON {}.veg_plantcover.attr_gml_id = {}.veg_plantcover_gen_intattribute.parentfk
                            WHERE attr_name='isBerry' AND gen_value=1
                  )""".format(self.schemaID, self.schemaID, self.schemaID, self.schemaID, self.schemaID)
        return self._pdm.getDataValue(request, float)

    def _get_count_tree_with_trunk_parameter(self, minDiameter, maxDiameter):
        request = """SELECT COUNT(*) FROM {}.veg_solitaryvegetationobject
                      WHERE veg_trunkdiameter_attr_uom='#cm' AND veg_trunkdiameter >= {} AND veg_trunkdiameter <= {};
                  """.format(self.schemaID, minDiameter, maxDiameter)
        return self._pdm.getDataValue(request, int)

    def _get_count_vegetary_attribute(self, filtered_class):
        request = """SELECT COUNT(attr_gml_id) FROM {}.veg_solitaryvegetationobject
                    WHERE veg_class='{}';""".format(self.schemaID, filtered_class)
        return self._pdm.getDataValue(request, int)

    def _get_count_vegetary_fruits_attribute(self):
        request = """SELECT COUNT(attr_gml_id) FROM {}.veg_solitaryvegetationobject
                      WHERE attr_gml_id IN (
                        SELECT parentfk FROM {}.veg_solitaryvegetationobject_gen_intattribute
                          WHERE attr_name='isFruit' AND gen_value=1
                  );""".format(self.schemaID, self.schemaID)
        return self._pdm.getDataValue(request, int)

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

    def _get_balcony_terrace_growing(self):
        request ="""SELECT SUM(gen_value) FROM {}.gen_genericcityobject_gen_doubleattribute
                      WHERE attr_name='area' AND gen_value>0 AND parentfk IN (
                        SELECT parentfk FROM {}.gen_genericcityobject_gen_intattribute
                          WHERE attr_name='isBalconyTerraceForGrowing' AND gen_value=1
                  );""".format(self.schemaID, self.schemaID)
        return self._pdm.getDataValue(request, float)

    def _get_shared_roof_terraces(self):
        request ="""SELECT SUM(gen_value) FROM {}.wtr_waterbody_gen_doubleattribute
                      WHERE attr_name='area' AND gen_value>0 AND parentfk IN (
                        SELECT parentfk FROM (
                          SELECT * FROM {}.wtr_waterbody_gen_intattribute
                            WHERE attr_name='isSharedRoofTerrace' AND gen_value=1
                        ) AS INTERMEDIATE GROUP BY parentfk HAVING count(parentfk) = 1
                  );""".format(self.schemaID, self.schemaID)
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

    def _get_bushes_experential(self):
        request ="""SELECT SUM(gen_value) FROM {}.veg_plantcover_gen_doubleattribute
                      WHERE attr_name='area' AND parentfk IN (
                        SELECT attr_gml_id FROM {}.veg_plantcover INNER JOIN {}.veg_plantcover_gen_intattribute ON
                          {}.veg_plantcover.attr_gml_id = {}.veg_plantcover_gen_intattribute.parentfk
                            WHERE attr_name='isExperiential' AND gen_value=1 AND veg_class='1080'
                  );""".format(self.schemaID, self.schemaID, self.schemaID, self.schemaID, self.schemaID)
        return self._pdm.getDataValue(request, float)

    def getData(self):
        self.responseData["Total land area"] = self._get_total_land_area()

        self.responseData["Unsupported ground greenery"] = self._get_unsupported_ground_greenery()
        self.responseData["Plant bed (>800 mm)"] = self._get_plant_bed_with_height(800, 100000)
        self.responseData["Plant bed (600 - 800 mm)"] = self._get_plant_bed_with_height(600, 800)
        self.responseData["Plant bed (200 - 600 mm)"] = self._get_plant_bed_with_height(200, 600)
        self.responseData["Green roof (>300 mm)"] = self._get_green_roof(300, 100000)
        self.responseData["Green roof (50 - 300 mm)"] = self._get_green_roof(50, 300)
        self.responseData["Greenery on walls"] = self._get_green_roof(50, 300)
        self.responseData["Balcony boxes"] = self._get_generic_count_attribute('ECD_GENCO_BALCONY_BOX')

        self.responseData['Diversity in the field layer'] = self._get_generic_sum_attribute('ECD_GENCO_DIVERSITY_FIELD_LAYER')
        self.responseData['Natural species selection'] = self._get_generic_sum_attribute('ECD_GENCO_NATURAL_SPECIES_SELECTION')
        self.responseData['Diversity on thin sedum roofs'] = self._get_generic_sum_attribute('ECD_GENCO_DIVERSITY_THIN_SEDUM_ROOF')
        self.responseData['Integrated balcony boxes with climbing plants'] = self._get_generic_sum_attribute('ECD_GENCO_INTEGRATED_BALCONY_BOX_CLIMBING')
        self.responseData['Butterfly restaurants'] = self._get_generic_count_attribute('ECD_GENCO_BUTTERFLY_RESTAURANT')
        self.responseData['General bushes'] = self._get_general_bushes()
        self.responseData['Berry bushes'] = self._get_berry_bushes()
        self.responseData['Large trees'] = self._get_count_tree_with_trunk_parameter(30, 100000)
        self.responseData['Medium large trees'] = self._get_count_tree_with_trunk_parameter(20, 30)
        self.responseData['Small trees'] = self._get_count_tree_with_trunk_parameter(16, 20)
        self.responseData['Oaks'] = self._get_count_vegetary_attribute('ECD_SOLVEG_OAK')
        self.responseData['Fruit trees'] = self._get_count_vegetary_fruits_attribute()
        self.responseData['Fauna depots'] = self._get_generic_count_attribute('ECD_GENCO_FAUNA_DEPOT')
        self.responseData['Beetle feeders'] = self._get_generic_count_attribute('ECD_GENCO_BEETLE_FEEDER')
        self.responseData['Bird feeders'] = self._get_generic_count_attribute('ECD_GENCO_BIRD_FEEDER')

        self.responseData['Grass area games'] = self._get_grass_ball_games()
        self.responseData['Grardening areas in yards'] = self._get_gardening_in_yards()
        self.responseData['Balconies and terraces prepared for growing'] = self._get_balcony_terrace_growing()
        self.responseData['Shared roof terraces'] = self._get_shared_roof_terraces()
        self.responseData['Visible green roofs'] = self._get_visible_green()
        self.responseData['Floral arrangements'] = self._get_floral_arrangement()
        self.responseData['Experiential values of bushes'] = self._get_bushes_experential()

        return self.responseData
