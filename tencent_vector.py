#!/usr/bin/env python3



import tcvectordb
from tcvectordb.model.document import Document, SearchParams, Filter
from tcvectordb.model.enum import FieldType, IndexType, MetricType, EmbeddingModel
from tcvectordb.model.index import Index, VectorIndex, FilterIndex, HNSWParams
from tcvectordb.model.collection import Embedding, UpdateQuery
from tcvectordb.model.enum import FieldType, IndexType, MetricType, ReadConsistency


def create():    
    #create a database client object
    client = tcvectordb.VectorDBClient(url='http://43.140.253.125:10002', username='root', key='Wb44QSziG48iHMx0vyHy92OVdxM5w1OrNKapvPdu', read_consistency=ReadConsistency.EVENTUAL_CONSISTENCY, timeout=30)
    db = client.create_database('db_team34')
    # -- index config        
    index = Index(
        FilterIndex(name='id', field_type=FieldType.String, index_type=IndexType.PRIMARY_KEY),
        VectorIndex(name='vector', dimension=768, index_type=IndexType.HNSW,metric_type=MetricType.COSINE, params=HNSWParams(m=16, efconstruction=200)),
        FilterIndex(name='word', field_type=FieldType.String, index_type=IndexType.FILTER)
        )
    # Embedding config
    ebd = Embedding(vector_field='vector', field='text', model=EmbeddingModel.BGE_BASE_ZH)
    # create a collection        
    coll = db.create_collection(
        name='symptom-emb',
        shard=1,
        replicas=2,
        description='this is a collection of test embedding',
        embedding=ebd,
        index=index
        )
    print(vars(coll))
def upsert():
	client = tcvectordb.VectorDBClient(url='http://43.140.253.125:10002', username='root', key='Wb44QSziG48iHMx0vyHy92OVdxM5w1OrNKapvPdu', read_consistency=ReadConsistency.EVENTUAL_CONSISTENCY, timeout=30)
	db = client.database('db_team34')
	coll = db.collection('symptom-emb')
	res = coll.upsert(
		documents=[
			Document(id='0001', text="心脏瓣膜畸形", word='心脏瓣膜畸形'),
			Document(id='0002', text="骨骼发育异常", word='骨骼发育异常'),
			Document(id='0003', text="智力发育迟缓", word='智力发育迟缓'),
			Document(id='0004', text="心悸", word='心悸'),
			Document(id='0005', text="胸闷", word='胸闷'),
			Document(id='0006', text="心跳过速", word='心跳过速'),
			Document(id='0007', text="头晕", word='头晕'),
			Document(id='0008', text="晕厥", word='晕厥'),
			Document(id='0009', text="气短", word='气短'),
			Document(id='00010', text="乏力", word='乏力'),
			Document(id='00011', text="食欲不振", word='食欲不振'),
			Document(id='00012', text="呼吸困难", word='呼吸困难'),
			Document(id='00013', text="胸痛", word='胸痛'),
			Document(id='00014', text="心绞痛", word='心绞痛'),
			Document(id='00015', text="意识丧失", word='意识丧失'),
			Document(id='00016', text="倒地", word='倒地'),
			Document(id='00017', text="气促", word='气促'),
			Document(id='00018', text="发热", word='发热'),
			Document(id='00019', text="多数患者无症状", word='多数患者无症状'),
			Document(id='00020', text="心慌", word='心慌'),
			Document(id='00021', text="出冷汗", word='出冷汗'),
			Document(id='00022', text="视力模糊", word='视力模糊'),
			Document(id='00023', text="心律不齐", word='心律不齐'),
			Document(id='00024', text="水肿", word='水肿'),
			Document(id='00025', text="心动过速", word='心动过速'),
			Document(id='00026', text="腿部水肿", word='腿部水肿'),
			Document(id='00027', text="头痛", word='头痛'),
			Document(id='00028', text="恶心", word='恶心'),
			Document(id='00029', text="呕吐", word='呕吐'),
			Document(id='00030', text="心率不规则", word='心率不规则'),
			Document(id='00031', text="心动过缓", word='心动过缓'),
			Document(id='00032', text="血脂升高", word='血脂升高'),
			Document(id='00033', text="腹胀", word='腹胀'),
			Document(id='00034', text="消化不良", word='消化不良'),
			Document(id='00035', text="肝肿大", word='肝肿大'),
			Document(id='00036', text="眩晕", word='眩晕'),
			Document(id='00037', text="恶心呕吐", word='恶心呕吐'),
			Document(id='00038', text="意识障碍", word='意识障碍'),
			Document(id='00039', text="关节痛", word='关节痛'),
			Document(id='00040', text="皮肤红斑", word='皮肤红斑'),
			Document(id='00041', text="杵状指（趾）", word='杵状指（趾）'),
			Document(id='00042', text="浮肿", word='浮肿'),
			Document(id='00043', text="心率过慢", word='心率过慢'),
			Document(id='00044', text="多尿", word='多尿'),
			Document(id='00045', text="多饮", word='多饮'),
			Document(id='00046', text="多食", word='多食'),
			Document(id='00047', text="消瘦", word='消瘦'),
			Document(id='00048', text="突然昏倒", word='突然昏倒'),
			Document(id='00049', text="面色苍白", word='面色苍白'),
			Document(id='00050', text="血压显著下降", word='血压显著下降'),
			Document(id='00051', text="突然出现的心悸", word='突然出现的心悸'),
			Document(id='00052', text="咳嗽", word='咳嗽'),
			Document(id='00053', text="疲劳", word='疲劳'),
			Document(id='00054', text="体重增加", word='体重增加'),
			Document(id='00055', text="双下肢水肿", word='双下肢水肿'),
			Document(id='00056', text="多数无症状", word='多数无症状'),
			Document(id='00057', text="偶尔出现心悸", word='偶尔出现心悸'),
			Document(id='00058', text="血压升高", word='血压升高'),
			Document(id='00059', text="心脏杂音", word='心脏杂音'),
			Document(id='00060', text="关节疼痛", word='关节疼痛'),
			Document(id='00061', text="乳头无法勃起和伸出", word='乳头无法勃起和伸出'),
			Document(id='00062', text="乳头软弱无力", word='乳头软弱无力'),
			Document(id='00063', text="乳糜浓度增高", word='乳糜浓度增高'),
			Document(id='00064', text="贫血", word='贫血'),
			Document(id='00065', text="腹泻", word='腹泻'),
			Document(id='00066', text="体重下降", word='体重下降'),
			Document(id='00067', text="颈静脉怒张", word='颈静脉怒张'),
			Document(id='00068', text="突然发生晕厥", word='突然发生晕厥'),
			Document(id='00069', text="咳痰", word='咳痰')
		],
		build_index=True
	)
def searchByText(value):
    topK=3
    res=[]
    client = tcvectordb.VectorDBClient(url='http://43.140.253.125:10002', username='root', key='Wb44QSziG48iHMx0vyHy92OVdxM5w1OrNKapvPdu', read_consistency=ReadConsistency.EVENTUAL_CONSISTENCY, timeout=30)
    db = client.database('db_team34')
    coll = db.collection('symptom-emb')
    doc_lists = coll.searchByText(
        embeddingItems=[value],
        params=SearchParams(ef=200),
        limit=3,
        retrieve_vector=False,
        output_fields=['word']
    )           
    for i, docs in enumerate(doc_lists.get("documents")):
        for doc in docs[:topK]:
            if doc.get("score")>0.9:
                 res.append(doc.get("word"))
    print(doc_lists.get("documents"))
    return res


if __name__ == "__main__":
    #create()
    upsert()
    searchByText("胸痛")
